#!/usr/bin/python3

__doc__ = """Convert DICOM images to JPG files, handling various pixel formats and modalities."""

import sys
import traceback
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pydicom as dicom
from PIL import Image
from pydicom.pixel_data_handlers.util import apply_voi_lut
from pydicom.uid import UID


def _to_uint8(img: np.ndarray) -> np.ndarray:
    """Normalize any dtype image to 0..255 uint8."""
    
    img = img.astype(np.float32, copy=False)
    finite = np.isfinite(img)
    if not finite.any():
        return np.zeros_like(img, dtype=np.uint8)
    vmin = img[finite].min()
    vmax = img[finite].max()
    if vmax <= vmin:
        return np.zeros_like(img, dtype=np.uint8)
    img = (img - vmin) / (vmax - vmin) * 255.0
    return img.clip(0, 255).astype(np.uint8)


def is_image_dataset(ds) -> bool:
    """True if the dataset contains any pixel data element."""
    
    return any(
        tag in ds for tag in ("PixelData", "FloatPixelData", "DoubleFloatPixelData")
    )


def try_extract_pdf(ds, out_path_base: Path) -> bool:
    """
    If this dataset is an Encapsulated PDF, extract the PDF payload
    as a .pdf next to where the JPG would be.
    """
    
    sop_name = UID(getattr(ds, "SOPClassUID", "")).name
    if "Encapsulated PDF" in sop_name and "EncapsulatedDocument" in ds:
        pdf_path = out_path_base.with_suffix(".pdf")
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_bytes(ds.EncapsulatedDocument)
        print(f"Extracted PDF -> {pdf_path.name}")
        return True
    return False


def index_image_instances(root: Path) -> Dict[str, Path]:
    """Map SOPInstanceUID -> file path for image datasets under root."""
    
    idx: Dict[str, Path] = {}
    for f in root.rglob("*.dcm"):
        if not f.is_file():
            continue
        try:
            # Fast read, no pixel decode
            ds = dicom.dcmread(f, stop_before_pixels=True, force=True)
            if "SOPInstanceUID" in ds and is_image_dataset(ds):
                idx[str(ds.SOPInstanceUID)] = f
        except Exception:
            # Ignore bad files while indexing
            pass
    return idx


def try_convert_pr_reference(
    ds, out_path_base: Path, index_map: Dict[str, Path], convert_fn
) -> bool:
    """
    If ds is a Presentation State that references an image available in index_map,
    convert that referenced image to JPG at out_path_base.
    """

    sop_name = UID(getattr(ds, "SOPClassUID", "")).name
    if "Presentation State" not in sop_name:
        return False
    try:
        for ref_series in getattr(ds, "ReferencedSeriesSequence", []):
            for ref_sop in getattr(ref_series, "ReferencedSOPSequence", []):
                ref_uid = str(getattr(ref_sop, "ReferencedSOPInstanceUID", ""))
                if ref_uid and ref_uid in index_map:
                    src_img = index_map[ref_uid]
                    jpg_path = out_path_base.with_suffix(".jpg")
                    print(
                        f"PR references {src_img.name} -> converting to {jpg_path.name}"
                    )
                    return convert_fn(src_img, jpg_path)
    except Exception:
        pass
    return False


def convert_dicom_to_jpg(dicom_path: Path, output_path: Path) -> bool:
    """Convert a single DICOM image to JPG. Returns True if written."""
    
    ds = dicom.dcmread(dicom_path, force=True)

    # Skip non-image DICOMs
    if not is_image_dataset(ds):
        print(f"Skipping (no pixel data): {dicom_path.name}")
        return False

    # Decode pixels (may require extra libs for compressed syntaxes)
    try:
        arr = ds.pixel_array  # pydicom uses available handlers
    except Exception as e:
        print(f"Failed to decode pixel data for {dicom_path.name}: {e}")
        print(
            "Hint: for JPEG/JPEG2000/deflated DICOMs, install:\n"
            '  pip install "pylibjpeg[all]" gdcm'
        )
        return False

    # Apply VOI LUT / windowing if present (keeps clinical brightness/contrast)
    try:
        arr = apply_voi_lut(arr, ds)
    except Exception:
        pass  # not all datasets have VOI LUT

    # Convert MONOCHROME1 (inverted) to MONOCHROME2 visual convention
    if getattr(ds, "PhotometricInterpretation", "").upper() == "MONOCHROME1":
        arr = np.max(arr) - arr

    # Handle multiframe: pick first frame by default (unless the last dim is color channels)
    if arr.ndim == 3 and arr.shape[0] > 1 and arr.shape[-1] not in (3, 4):
        arr = arr[0]

    # Build PIL image depending on shape
    if arr.ndim == 2:  # grayscale
        img8 = _to_uint8(arr)
        pil_img = Image.fromarray(img8, mode="L")
    elif arr.ndim == 3 and arr.shape[-1] in (3, 4):  # color RGB(A)
        if arr.dtype != np.uint8:
            arr = _to_uint8(arr)
        if arr.shape[-1] == 4:  # drop alpha
            arr = arr[:, :, :3]
        pil_img = Image.fromarray(arr, mode="RGB")
    else:
        print(f"Unsupported pixel shape {arr.shape} in {dicom_path.name}, skipping.")
        return False

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pil_img.save(output_path, format="JPEG", quality=95)
    return True


def run(input_dir: Path, output_dir: Path):
    input_dir = Path(input_dir).expanduser().resolve()
    output_dir = Path(output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build an index of available image instances for PR following
    print("Indexing image instances (for PR references)...")
    image_index = index_image_instances(input_dir)
    print(f"Indexed {len(image_index)} image instances.\n")

    processed = skipped = failed = extracted_pdfs = pr_converted = 0
    skipped_info: List[Tuple[str, str, str]] = []

    # Recurse; match .dcm case-insensitively
    for dicom_file in input_dir.rglob("*"):
        if not dicom_file.is_file():
            continue
        if dicom_file.suffix.lower() != ".dcm":
            continue

        rel = dicom_file.relative_to(input_dir)
        out_path = output_dir / rel.with_suffix(".jpg")

        try:
            ds_head = dicom.dcmread(dicom_file, stop_before_pixels=True, force=True)
            sop_name = (
                UID(getattr(ds_head, "SOPClassUID", "")).name or "Unknown SOP Class"
            )
            modality = getattr(ds_head, "Modality", "Unknown")
        except Exception:
            ds_head = None
            sop_name = "Unknown SOP Class"
            modality = "Unknown"

        print(f"Processing {rel}")

        try:
            ds = dicom.dcmread(dicom_file, force=True)

            if is_image_dataset(ds):
                print(f"  Converting -> {out_path.relative_to(output_dir)}")
                ok = convert_dicom_to_jpg(dicom_file, out_path)
                if ok:
                    processed += 1
                else:
                    skipped += 1
                continue

            # Non-image: try PDF extract
            if try_extract_pdf(ds, out_path):
                extracted_pdfs += 1
                continue

            # Non-image: try PR follow
            if try_convert_pr_reference(
                ds, out_path, image_index, convert_dicom_to_jpg
            ):
                pr_converted += 1
                continue

            # Otherwise, skip with classification
            skipped += 1
            skipped_info.append((rel.as_posix(), modality, sop_name))
            print(f"  Skipping (no pixel data): [{modality} | {sop_name}]")

        except Exception:
            failed += 1
            print(f"Unexpected failure on {dicom_file.name}")
            traceback.print_exc(file=sys.stdout)

    # Summary
    print("\nSummary:")
    print(f"  Wrote JPGs:          {processed}")
    print(f"  Extracted PDFs:      {extracted_pdfs}")
    print(f"  PR-referenced JPGs:  {pr_converted}")
    print(f"  Skipped:             {skipped}")
    print(f"  Failed:              {failed}")

    if skipped_info:
        print("\nSkipped (no pixel data):")
        for path, modality, sop in skipped_info:
            print(f"  - {path}  [{modality} | {sop}]")


if __name__ == "__main__":
    input_dir = input("Enter input directory (with DICOM files): ").strip()
    output_dir = input("Enter output directory (for JPG files): ").strip()
    run(Path(input_dir), Path(output_dir))

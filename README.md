## Description

This repository contains software for converting local .dcm files to .pdf or .jpg.

## Dependencies

- [Python 3.11+](https://www.python.org/downloads/)
- [GitHub CLI](https://cli.github.com/)
- Basic shell skills (e.g. bash), i.e. traversing and creating directories
- Basic Python skills, i.e. [creating a virtual environment](https://docs.python.org/3/library/venv.html)

## Installation

Run the following command to clone this repository:

```bash
gh repo clone michaelthomasletts/dcm-to-jpg
```

Install the Python dependencies like so:

```bash
pip install -r requirements.txt
```

## Usage

Use the script like this:

```bash
cd dcm-to-jpg
python3 -m image_script
```

You will be prompted, as shown below, to provide the local directories where your .dcm images are saved and where you'd like your .pdf and .jpg files to be saved.

```bash
Enter input directory (with DICOM files): <input dir>
Enter output directory (for JPG files): <output dir>
```

When finished, you will see a summary message like this:

```txt
Summary:
  Wrote JPGs:          7
  Extracted PDFs:      3
  PR-referenced JPGs:  0
  Skipped:             0
  Failed:              0
```

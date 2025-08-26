## What is this?

This repository contains software for converting local .dcm files to .pdf or .jpg.

.dcm is a common file format for medical doctors and medical institutions. Thus, modern medical institutions tend to store and share patient images and documents in .dcm format, e.g. [NYU Langone's MyChart](https://mychart.nyulmc.org/mychart). 

Opening and reading .dcm files, however, requires specialized software that patients almost certainly do not have access to. Although there are online tools for converting .dcm > .jpg or .dcm > .pdf, patients may not feel comfortable sharing their medically sensitive data with unknown developers. Which leaves patients in a difficult position. 

Using this software, you can convert .dcm files to .pdf or .jpg without anxiety about your medically sensitive data getting in the wrong hands.

## Who is this software for?

**This tool requires a bit of technical knowledge.** If you are not technically adept then you may want to use [this LLM agent to guide you through using it on your computer](https://chatgpt.com/g/g-68add9b82bec8191942c7da5a6273b13-dcm-to-pdf-or-jpg-converter). 

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

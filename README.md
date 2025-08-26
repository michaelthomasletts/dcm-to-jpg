```markdown
#####    ##   ##   #####            #######   #####                 ##  ######    #####   
### ##   ### ###  ###  ##           #######  ###  ##                ##  ###  ##  ###      
###  ##  #######  ##                #######  ###  ##           ###  ##  ###  ##  ### ##   
###  ##  #######  ##   ##             ###    ###  ##           ###  ##  #######  ###  ##  
### ###  #######  ###  ##             ###    ###  ##           ###  ##  ######   ###  ##  
#######  ###  ##  #######             ###    #######           #######  ####     #######  
#######  ###  ##  #######             ###    #######           #######  ####     #######  
######   ###  ##   #####              ###     #####             #####   ####      #####   
```

## Description

This repository contains software for converting local .dcm files to .pdf or .jpg.

.dcm is a common file format for doctors and hospitals to store and share patient images and documents, e.g. [NYU Langone's MyChart](https://mychart.nyulmc.org/mychart). 

## Security and Acessibility

Opening and reading .dcm files requires specialized software that patients rarely have. 

Although there are online tools for converting .dcm -> .jpg or .dcm -> .pdf, patients may not feel comfortable sharing their medically sensitive data with unknown developers. Which leaves patients in a difficult position. 

By using this software on your personal computer, you can convert .dcm files to .pdf or .jpg with 100% confidence about your medically sensitive data not getting into the wrong hands.

**This tool requires a bit of technical knowledge.** If you are not technically adept then you may want to use [this LLM agent to guide you through using this software on your computer locally](https://chatgpt.com/g/g-68add9b82bec8191942c7da5a6273b13-dcm-to-pdf-or-jpg-converter). 

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

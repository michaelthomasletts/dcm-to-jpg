```txt
     #                        #                      #                
     #                        #                                       
  ## #   ###   ## #          ####    ###            ##   # ##    ## # 
 #  ##  #   #  # # #          #     #   #            #   ##  #  #  #  
 #   #  #      # # #          #     #   #            #   ##  #   ##   
 #  ##  #   #  # # #          #  #  #   #            #   # ##   #     
  ## #   ###   #   #           ##    ###          #  #   #       ###  
                                                  #  #   #      #   # 
                                                   ##    #       ###  
```

## Description

This repository contains software for converting local .dcm files to .pdf or .jpg.

.dcm is a common file format for doctors and hospitals to store and share patient images and documents, e.g. [NYU Langone's MyChart](https://mychart.nyulmc.org/mychart). 

## Security and Acessibility

Opening and reading .dcm files requires specialized software that patients rarely have. If ever.

Although there are online tools for converting .dcm -> .jpg or .dcm -> .pdf, patients may not feel comfortable sharing their medically sensitive data with unknown developers. Frankly, they _should not_ feel comfortable doing that! Which leaves patients in a difficult position . . . How do you open a fancy .dcm file without the software to do so, and none of the online file converters seem totally trustworthy . . . ? 😬 

By using this software on your personal computer, you can convert .dcm files to .pdf or .jpg with 100% confidence about your medically sensitive data not getting into the wrong hands. A few extra minutes of effort could save you a lot in peace of mind and security.

**Disclaimer: this tool requires a bit of technical knowledge.** If you are not technically adept then you may want to use [this LLM agent to guide you through using this software on your computer locally](https://chatgpt.com/g/g-68add9b82bec8191942c7da5a6273b13-dcm-to-pdf-or-jpg-converter). It's friendly! 😃

## Dependencies

- [Python 3.11+](https://www.python.org/downloads/)
- [GitHub CLI](https://cli.github.com/)

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

Store your .dcm files somewhere on your local machine, and navigate to where those files are saved from your terminal. Ideally, keep those images in the same directory as where you cloned this repository.

Then, use the script like this:

```bash
cd dcm-to-jpg
python3 -m script
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

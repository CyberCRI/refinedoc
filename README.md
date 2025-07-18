# Refinedoc
 Python library for extracting headers, footers and body from PDF post parsing file by [the Learning Planet Institute.](https://www.learningplanetinstitute.org/) 

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Table of Contents


## Why using Refinedoc ?
The idea behind this library is to enable post-extraction processing of unstructured text content, the best-known example being pdf files. 
The main idea is to robustly and securely separate the text body from its headers and footers.

What's more, the lib is written in pure Python and has no dependencies other than the standard lib.


## Features
- **Header and Footer Extraction**: Automatically identifies and extracts headers and footers from the document.
- **Body Extraction**: Separates the main content of the document from headers and footers.
- **Page Association**: Uses page association techniques to ensure accurate extraction of headers and footers across multiple pages.
- **Robustness**: Designed to handle various document structures and formats, ensuring reliable extraction even in complex layouts.
- **Pure Python Implementation**: No external dependencies, making it easy to integrate into existing Python projects.
- **Easy to Use**: Simple API for extracting headers, footers, and body content from documents.
- **Compatibility**: Works with text extracted from PDF files using libraries like PyPDF, PyMuPDF, and pdfplumber.
- **Performance**: Efficiently processes large documents with minimal overhead.
- **Open Source**: Licensed under Apache 2.0, allowing for free use and modification in both personal and commercial projects.

## Quickstart
### Requirements
- Python 3.10 <=
### Installation
You can install with pip
```
pip install refinedoc
```
### Example (vanilla)

```python
from refinedoc.refined_document import RefinedDocument

document = [
            [
                "header 1",
                "subheader 1",
                "lorem ipsum dolor sit amet",
                "consectetur adipiscing elit",
                "footer 1",
            ],
            [
                "header 2",
                "subheader 2",
                "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
                "footer 2",
            ],
            [
                "header 3",
                "subheader 3",
                "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
                "footer 3",
            ],
            [
                "header 4",
                "subheader 4",
                "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
                "footer 4",
            ],
        ]

rd = RefinedDocument(content=document)
headers = rd.headers
# [["header 1", "subheader 1"], ["header 2", "subheader 2"], ["header 3", "subheader 3"], ["header 4", "subheader 4"]]

footers = rd.footers
# [["footer 1"], ["footer 2"], ["footer 3"], ["footer 4"]]

body = rd.body
# [["lorem ipsum dolor sit amet", "consectetur adipiscing elit"], ["sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"], ["ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat"], ["duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur"]]
```

## Example (with pypdf)

```python
from refinedoc.refined_document import RefinedDocument
from pypdf import PdfReader

# Build the document from a PDF file
reader = PdfReader("path/to/your/pdf/file.pdf")
document = []
for page in reader.pages:
    document.append(page.extract_text().split("\n"))
    
rd = RefinedDocument(content=document)
headers = rd.headers
# [["header 1", "subheader 1"], ["header 2", "subheader 2"], ["header 3", "subheader 3"], ["header 4", "subheader 4"]]
footers = rd.footers
# [["footer 1"], ["footer 2"], ["footer 3"], ["footer 4"]]
body = rd.body
# [["lorem ipsum dolor sit amet", "consectetur adipiscing elit"], ["sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"], ["ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat"], ["duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur"]]
```

## Example (with pymupdf)

```python
from refinedoc.refined_document import RefinedDocument
import pymupdf  # PyMuPDF

# Build the document from a PDF file
doc = fitz.open("path/to/your/pdf/file.pdf")
document = []
for page in doc:
    text = page.get_text("text").split("\n")
    document.append(text)
    
rd = RefinedDocument(content=document)
headers = rd.headers
# [["header 1", "subheader 1"], ["header 2", "subheader 2"], ["header 3", "subheader 3"], ["header 4", "subheader 4"]]
footers = rd.footers
# [["footer 1"], ["footer 2"], ["footer 3"], ["footer 4"]]
body = rd.body
# [["lorem ipsum dolor sit amet", "consectetur adipiscing elit"], ["sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"], ["ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat"], ["duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur"]]
```

## Example (with pdfplumber)

```python
from refinedoc.refined_document import RefinedDocument
import pdfplumber

# Build the document from a PDF file
with pdfplumber.open("path/to/your/pdf/file.pdf") as pdf:
    document = []
    for page in pdf.pages:
        text = page.extract_text().split("\n")
        document.append(text)
        
rd = RefinedDocument(content=document)
headers = rd.headers
# [["header 1", "subheader 1"], ["header 2", "subheader 2"], ["header 3", "subheader 3"], ["header 4", "subheader 4"]]
footers = rd.footers
# [["footer 1"], ["footer 2"], ["footer 3"], ["footer 4"]]
body = rd.body
# [["lorem ipsum dolor sit amet", "consectetur adipiscing elit"], ["sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"], ["ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat"], ["duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur"]]
```

## Advanced usage
### Improving speed
You can improve the speed of extraction by using `ratio_speed` parameter when instantiating class.
Ratio speed is an integer between 1 and 3. More the ratio is high, more the extraction will be fast but less accurate.

These ratio are proxy for parameter from SequenceMatcher from difflib library.
- `ratio_speed=1` is equivalent to using regular [ratio](https://docs.python.org/3.12/library/difflib.html#difflib.SequenceMatcher.ratio)
- `ratio_speed=2` is equivalent to using [quick_ratio](https://docs.python.org/3.12/library/difflib.html#difflib.SequenceMatcher.quick_ratio)
- `ratio_speed=3` is equivalent to using [real_quick_ratio](https://docs.python.org/3.12/library/difflib.html#difflib.SequenceMatcher.real_quick_ratio)

```python
RefinedDocument(content=document, ratio_speed=2)
``` 

### Customize windows size
The win parameter in the RefinedDocument class defines the size of the window used to detect similar headers and footers between pages in the document. 
When separating headers/footers, it determines how many neighbouring pages (before and after the current page) are taken into account to compare and identify repetitive lines. 
A larger value increases the scope of the comparison, which can improve detection but slow down processing.

```python
from refinedoc.refined_document import RefinedDocument

# 10 pages before and after the current page will be considered for 
# header/footer detection
RefinedDocument(content=document, win=10)
```
## How it's work

My work is based on this paper : [Lin, Xiaofan. (2003). Header and Footer Extraction by Page-Association. 5010. 164-171. 10.1117/12.472833. ](https://www.researchgate.net/publication/221253782_Header_and_Footer_Extraction_by_Page-Association)

And an [article medium by Hussain Shahbaz Khawaja](https://medium.com/@hussainshahbazkhawaja/paper-implementation-header-and-footer-extraction-by-page-association-3a499b2552ae).

# License
This projects is licensed under Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

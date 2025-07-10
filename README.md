# Refinedoc
Python library for post-extraction refinement of text that may be derived from PDF extraction by [the Learning Planet Institute.](https://www.learningplanetinstitute.org/) 

[![PyPI version](https://badge.fury.io/py/refinedoc.svg?icon=si%3Apython)](https://badge.fury.io/py/refinedoc)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Why using Refinedoc ?
The idea behind this library is to enable post-extraction processing of unstructured text content, the best-known example being pdf files. 
The main idea is to robustly and securely separate the text body from its headers and footers.

What's more, the lib is written in pure Python and has no dependencies other than the standard lib.

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

## How it's work

My work is based on this paper : [Lin, Xiaofan. (2003). Header and Footer Extraction by Page-Association. 5010. 164-171. 10.1117/12.472833. ](https://www.researchgate.net/publication/221253782_Header_and_Footer_Extraction_by_Page-Association)

And an [article medium by Hussain Shahbaz Khawaja](https://medium.com/@hussainshahbazkhawaja/paper-implementation-header-and-footer-extraction-by-page-association-3a499b2552ae).

# License
This projects is licensed under Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

# Refinedoc
Python library for post-extraction refinement of text that may be derived from PDF extraction.

[![PyPI version](https://badge.fury.io/py/refinedoc.svg?icon=si%3Apython)](https://badge.fury.io/py/refinedoc)

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
### Example
```python

```

## How it's work

My work is based on this paper : [Lin, Xiaofan. (2003). Header and Footer Extraction by Page-Association. 5010. 164-171. 10.1117/12.472833. ](https://www.researchgate.net/publication/221253782_Header_and_Footer_Extraction_by_Page-Association)

And an [article medium by Hussain Shahbaz Khawaja](https://medium.com/@hussainshahbazkhawaja/paper-implementation-header-and-footer-extraction-by-page-association-3a499b2552ae).
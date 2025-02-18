<div id="top" align="left">

<!-- HEADER -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/eli64s/pdflex/656aa96e7c4b65ca72077d170e4dcdbdd9bbbc45/docs/assets/logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eli64s/pdflex/656aa96e7c4b65ca72077d170e4dcdbdd9bbbc45/docs/assets/logo-light.svg">
  <img alt="pdflex Logo" src="https://raw.githubusercontent.com/eli64s/pdflex/656aa96e7c4b65ca72077d170e4dcdbdd9bbbc45/docs/assets/logo-light.svg" width="100%" style="max-width: 100%;">
</picture>

<!-- BADGES -->
<div align="left">
  <p align="left" style="margin-bottom: 20px;">
    <a href="https://github.com/eli64s/pdflex/actions">
      <img src="https://img.shields.io/github/actions/workflow/status/eli64s/pdflex/ci.yml?label=CI&style=flat&logo=githubactions&logoColor=white&labelColor=2A2A2A&color=FF1493" alt="GitHub Actions" />
    </a>
    <a href="https://app.codecov.io/gh/eli64s/pdflex">
      <img src="https://img.shields.io/codecov/c/github/eli64s/pdflex?label=Coverage&style=flat&logo=codecov&logoColor=white&labelColor=2A2A2A&color=00F5FF" alt="Coverage" />
    </a>
    <a href="https://pypi.org/project/pdflex/">
      <img src="https://img.shields.io/pypi/v/pdflex?label=PyPI&style=flat&logo=pypi&logoColor=white&labelColor=2A2A2A&color=3d8be1" alt="PyPI Version" />
    </a>
    <a href="https://github.com/eli64s/pdflex">
      <img src="https://img.shields.io/pypi/pyversions/pdflex?label=Python&style=flat&logo=python&logoColor=white&labelColor=2A2A2A&color=9b26d4" alt="Python Version" />
    </a>
    <a href="https://opensource.org/license/mit/">
      <img src="https://img.shields.io/github/license/eli64s/pdflex?label=License&style=flat&logo=opensourceinitiative&logoColor=white&labelColor=2A2A2A&color=4B0082" alt="MIT License">
    </a>
  </p>
</div>

<div align="left">
  <img src="https://raw.githubusercontent.com/eli64s/pdflex/d545ac98f5ad59ece892e638a7d3bdee593d8e88/docs/assets/line.svg" alt="thematic-break" width="100%" height="2px" style="margin: 20px 0;">
</div>

</div>

## What is `PDFlex?`

PDFlex is a powerful PDF processing toolkit for Python. It provides robust tools for PDF validation, text extraction, merging (with custom separator pages), searching, and more—all built to streamline your PDF automation workflows.

## Features

- **PDF Validation:** Quickly verify if a file is a valid PDF.
- **Text Extraction:** Extract text from PDFs using either PyMuPDF or PyPDF.
- **Directory Processing:** Process entire directories of PDFs for text extraction.
- **PDF Merging:** Merge multiple PDF files into one, automatically inserting a custom separator page between documents.
  - The separator page displays the title (derived from the filename) with underscores and hyphens removed.
  - Supports both portrait and landscape separator pages (ideal for lecture slides).
- **PDF Searching:** Recursively search for PDFs in a directory based on filename patterns (e.g., numeric float prefixes).


<!-- ## Documentation

Full documentation is available at [https://pdflex.readthedocs.io/](https://pdflex.readthedocs.io/)

- [User Guide](https://pdflex.readthedocs.io/en/latest/user_guide.html)
- [API Reference](https://pdflex.readthedocs.io/en/latest/api.html)
- [Examples](https://pdflex.readthedocs.io/en/latest/examples.html) -->

---

## Quick Start

## Installation

PDFlex is available on PyPI. To install using pip:

```bash
pip install -U pdflex
```

Alternatively, install in an isolated environment with pipx:

```bash
pipx install pdflex
```

For the fastest installation using uv:

```bash
uv tool install pdflex
```

---

## Usage

### Command-Line Interface (CLI)

PDFlex provides a convenient CLI for merging and searching PDFs. The CLI supports two primary commands: `merge` and `search`.

#### Merge Command

Merge multiple PDF files into a single document while automatically inserting a separator page before each document.

**Usage:**

```bash
pdflex merge /path/to/file1.pdf /path/to/file2.pdf -o merged_output.pdf
```

Add the `--landscape` flag to create separator pages in landscape orientation:

```bash
pdflex merge /path/to/file1.pdf /path/to/file2.pdf -o merged_output.pdf --landscape
```

#### Search and Merge Command

Search for PDF files in a directory based on filename filters (or search for lecture slides with numeric float prefixes) and merge them into one PDF.

**Usage:**

- **General Search:**

  ```bash
  pdflex search /path/to/search -o merged_output.pdf --prefix "Chapter" --suffix ".pdf"
  ```

- **Lecture Slides Merge:**
  (Merges all PDFs whose filenames start with a numeric float prefix like `1.2_`, `3.2_`, etc., in sorted order. Separator pages will be in landscape orientation.)

  ```bash
  pdflex search /path/to/algorithms-and-computation -o merged_lectures.pdf --lecture
  ```

### Python API Usage

You can also use PDFlex directly from your Python code. Below are examples for some common tasks.

#### Merging PDFs with Separator Pages

```python
from pathlib import Path
from pdflex.merge import merge_pdfs

# List of PDF file paths to merge
pdf_files = [
    "/path/to/document1.pdf",
    "/path/to/document2.pdf"
]

# Merge files, using landscape separator pages (ideal for lecture slides)
merge_pdfs(pdf_files, output_path="merged_output.pdf", landscape=True)
```

#### Searching for PDFs by Filename

```python
from pdflex.search import search_pdfs, search_numeric_prefixed_pdfs

# General search: Find PDFs that start with a prefix and/or end with a suffix
pdf_list = search_pdfs("/path/to/search", prefix="Chapter", suffix=".pdf")
print("Found PDFs:", pdf_list)

# Lecture slides: Find PDFs with numeric float prefixes (e.g., "1.2_Intro.pdf")
lecture_slides = search_numeric_prefixed_pdfs("/path/to/algorithms-and-computation")
print("Found lecture slides:", lecture_slides)
```

<!--
#### Extracting Text from a PDF

```python
from pdflex import extract_text_from_pdf

# Extract text from a PDF using the auto-detection method (tries PyMuPDF then falls back to PyPDF)
output_txt = extract_text_from_pdf("invoice.pdf", method="auto")
print(f"Extracted text saved to: {output_txt}")
```

#### Processing an Entire Directory

```python
from pdflex import process_directory

# Process all PDFs in a directory and extract their text to corresponding .txt files.
process_directory("/path/to/pdf_directory", output_dir="/path/to/text_outputs")
```

---

## API Reference

For detailed API documentation, please refer to the [API Reference](https://pdflex.readthedocs.io/en/latest/api.html).

### Exceptions

- **PDFlexError:** Raised for any error during PDF processing (e.g., invalid PDF, extraction failure).

### Modules Overview

- **`pdflex.merge`**
  Contains functions to merge PDFs, insert separator pages (with customizable orientation and title cleaning), and write the final merged document.

- **`pdflex.search`**
  Provides functions to recursively search for PDFs in a directory based on filename patterns, including numeric float prefixes for lecture slides.

- **`pdflex.extract`** (and similar)
  Functions for extracting text using PyMuPDF or PyPDF, validating PDF files, and processing directories of PDFs.

- **`pdflex.cli`**
  Command-line interface that exposes the `merge` and `search` commands, complete with rich console output.
-->

---

## Contributing

Contributions are welcome! Whether it's bug reports, feature requests, or code contributions, please feel free to:

1. Open an [issue][github-issues]
2. Submit a [pull request][github-pulls]
3. Improve documentation.
4. Share your ideas!

---

## Acknowledgments

This project is built upon several awesome PDF open-source projects:

- [pypdf](https://github.com/pymupdf/PyMuPDF)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [reportlab](https://www.reportlab.com/opensource/)

---

## License

PDFlex is released under the [MIT][mit-license] license. <br />
Copyright (c) 2020 to present [PDFlex][pdflex] and contributors.

<div align="left">
  <a href="#top">
    <img src="https://raw.githubusercontent.com/eli64s/pdflex/607d295f58914fc81a5b71fd994af90901b6433c/docs/assets/button.svg" width="100px" height="100px" alt="Return to Top">
  </a>
</div>

<div align="left">
  <img src="https://raw.githubusercontent.com/eli64s/pdflex/d545ac98f5ad59ece892e638a7d3bdee593d8e88/docs/assets/line.svg" alt="thematic-break" width="100%" height="2px" style="margin: 20px 0;">
</div>

<!-- REFERENCE LINKS -->

<!-- PROJECT RESOURCES -->
[pypi]: https://pypi.org/project/pdflex/
[pdflex]: https://github.com/eli64s/pdflex
[github-issues]: https://github.com/eli64s/pdflex/issues
[github-pulls]: https://github.com/eli64s/pdflex/pulls
[mit-license]: https://github.com/eli64s/pdflex/blob/main/LICENSE
[examples]: https://github.com/eli64s/pdflex/tree/main/docs/examples

<!-- DEV TOOLS -->
[python]: https://www.python.org/
[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pipx.pypa.io/stable/
[uv]: https://docs.astral.sh/uv/
[mkdocs]: https://www.mkdocs.org/
[mkdocs.yml]: https://www.mkdocs.org/user-guide/configuration/

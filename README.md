<div id="top" align="left">

<!-- HEADER -->
<!-- 
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/eli64s/pdflex/ed2534164a2f7f2a7b4aafef998127791b205f30/docs/assets/logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eli64s/pdflex/ed2534164a2f7f2a7b4aafef998127791b205f30/docs/assets/logo-light.svg">
  <img alt="pdflex Logo" src="https://raw.githubusercontent.com/eli64s/pdflex/ed2534164a2f7f2a7b4aafef998127791b205f30/docs/assets/logo-light.svg" width="900" style="max-width: 100%;">
</picture>
-->

<div>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 240">
      <!-- Gradients -->
      <defs>
          <linearGradient id="textGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="33%" style="stop-color: #FF1493" />
              <stop offset="67%" style="stop-color: #00F5FF" />
              <stop offset="100%" style="stop-color: #4B0082" />
          </linearGradient>
          <!-- Background pattern -->
          <pattern id="gridPattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
              <rect width="20" height="20" fill="none" />
              <circle cx="10" cy="10" r="1" fill="#E2E8F0" opacity="0.2" />
          </pattern>
      </defs>
      <!-- Background -->
      <rect width="100%" height="100%" fill="white" />
      <rect width="100%" height="100%" fill="url(#gridPattern)" />
      <!-- Main Text Group - Moved to left edge -->
      <g transform="translate(20, 120)">
          <!-- PDF Text -->
          <text x="0" y="0" font-family="Arial, sans-serif" font-size="84" font-weight="bold" fill="url(#textGradient)">
            <tspan>PDFlex</tspan>
            <!-- <tspan fill="#7934C5">FLEX</tspan> -->
          </text>
          <!-- Animated underline -->
          <rect x="0" y="10" width="360" height="4" fill="url(#textGradient)">
              <animate attributeName="width" values="0;360;360" dur="1.5s" begin="0s" fill="freeze" />
          </rect>
      </g>
      <!-- Tagline - Aligned with text -->
      <text x="20" y="164" font-family="Arial, sans-serif" font-size="22" fill="#7934C5" opacity="0.8">
          Python tools for PDF automation
      </text>
      <!-- Sub tagline - Aligned with text -->
      <text x="20" y="190" font-family="Arial, sans-serif" font-size="16" fill="#7934C5" opacity="0.6">
          Convert | Extract | Merge | Transform
      </text>
      <!-- Decorative Elements - Adjusted position -->
      <g transform="translate(440, 100)">
          <!-- Stylized document icon -->
          <path d="M20,0 L50,0 L70,20 L70,90 L20,90 Z" fill="none" stroke="url(#textGradient)" stroke-width="2">
              <animate attributeName="stroke-dasharray" from="200" to="0" dur="2s" fill="freeze" />
          </path>
          <path d="M50,0 L50,20 L70,20" fill="none" stroke="url(#textGradient)" stroke-width="2" />
      </g>
  </svg>
</div>

<!-- <h3 align="left">
  Powerful Tools for Modern Documentation
</h3>

<p align="left">
  <em>A powerful toolkit for transforming, validating, and managing your Markdown documentation.</em>
</p> -->

<!-- BADGES -->
<div align="left">
  <p align="left" style="margin-bottom: 20px;">
    <a href="https://github.com/eli64s/pdflex/actions">
      <img src="https://img.shields.io/github/actions/workflow/status/eli64s/pdflex/ci.yml?label=CI&style=flat&logo=githubactions&logoColor=white&labelColor=2A2A2A&color=FF1493" alt="GitHub Actions" />
    </a>
    <a href="https://app.codecov.io/gh/eli64s/pdflex">
      <img src="https://img.shields.io/codecov/c/github/eli64s/pdflex?label=Coverage&style=flat&logo=codecov&logoColor=white&labelColor=2A2A2A&color=00F5FF" alt="Coverage" />
    </a>
    <!-- <a href="https://pypi.org/project/pdflex/">
      <img src="https://img.shields.io/pypi/v/pdflex?label=PyPI&style=flat&logo=pypi&logoColor=white&labelColor=2A2A2A&color=3d8be1" alt="PyPI Version" />
    </a>
    <a href="https://github.com/eli64s/pdflex">
      <img src="https://img.shields.io/pypi/pyversions/pdflex?label=Python&style=flat&logo=python&logoColor=white&labelColor=2A2A2A&color=9b26d4" alt="Python Version" />
    </a> -->
    <a href="https://opensource.org/license/mit/">
      <img src="https://img.shields.io/github/license/eli64s/pdflex?label=License&style=flat&logo=opensourceinitiative&logoColor=white&labelColor=2A2A2A&color=4B0082" alt="MIT License">
    </a>
  </p>
</div>

<div align="left">
<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="4">
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="33%" style="stop-color: #FF1493" />
            <stop offset="67%" style="stop-color:#00F5FF" />
            <stop offset="100%" style="stop-color:#4B0082" />
        </linearGradient>
    </defs>
    <rect width="100%" height="2.5" fill="url(#grad1)" />
</svg>
</div>

</div>
<!-- HEADER END -->

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

PDFlex is released under the [MIT][mit-license] license.
Copyright (c) 2020 to present [PDFlex][pdflex] and contributors.

<div align="left">
  <a href="#top">
    <img src="docs/assets/button.svg" width="100px" height="100px" alt="Return to Top">
  </a>
</div>

<div align="left">
<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="4">
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="33%" style="stop-color: #FF1493" />
            <stop offset="67%" style="stop-color:#00F5FF" />
            <stop offset="100%" style="stop-color:#4B0082" />
        </linearGradient>
    </defs>
    <rect width="100%" height="2.5" fill="url(#grad1)" />
</svg>
</div>

<!-- <div align="center">
  <img src="https://raw.githubusercontent.com/eli64s/pdflex/216a92894e6f30c707a214fad5a5fba417e3bc39/docs/assets/line.svg" alt="separator" width="100%" height="2px" style="margin: 20px 0;">
</div> -->

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

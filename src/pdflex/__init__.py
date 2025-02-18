"""
PDFlex: Python tools for PDF automation.
============================================

PDFlex provides tools for extracting, modifying, and analyzing PDF documents.

Main Components:
---------------
- ...

Basic Usage:
-----------
>>> ...
>>> ...
"""

from importlib.metadata import version

from .exceptions import (
    ExtractionError,
    PDFlexError,
    ReplacementError,
    ValidationError,
)
from .merge import merge_pdfs
from .search import search_numeric_prefixed_pdfs, search_pdfs
from .slides_to_text import extract_text_from_pdf, process_directory

__version__ = version("pdflex")

__all__ = [
    "ExtractionError",
    "PDFlexError",
    "ReplacementError",
    "ValidationError",
    "extract_text_from_pdf",
    "merge_pdfs",
    "process_directory",
    "search_numeric_prefixed_pdfs",
    "search_pdfs",
]

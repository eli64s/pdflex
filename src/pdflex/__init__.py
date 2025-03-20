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

from .exceptions import PDFlexError
from .merge import merge_pdfs
from .search import search_numeric_prefixed_pdfs, search_pdfs

__version__ = version("pdflex")

__all__ = [
    "PDFlexError",
    "merge_pdfs",
    "search_numeric_prefixed_pdfs",
    "search_pdfs",
]

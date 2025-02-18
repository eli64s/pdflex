"""
PDFlex: A comprehensive PDF processing library
============================================

PDFlex provides tools for extracting, modifying, and analyzing PDF documents.

Main Components:
---------------
- Extractors: Extract structured data from PDFs
- Modifiers: Modify PDF content
- Converters: Convert PDFs to other formats
- Features: Additional PDF processing capabilities

Basic Usage:
-----------
>>> from pdflex import extract_text, process_directory
>>> extract_text("document.pdf", "output.txt")
"""

from importlib.metadata import version
from pathlib import Path
from typing import Any, Dict, Union

# Utilities
from .exceptions import (
    ExtractionError,
    PDFlexError,
    ReplacementError,
    ValidationError,
)

# Data extraction
from .extractors.patterns import (
    BaseExtractor,
    ExtractionPattern,
    PDFDataExtractor,
    RegexExtractor,
)
from .merge import merge_pdfs

# Text replacement
from .modifiers.text_replacement import (
    PDFTextReplacer,
    ReplacementRule,
    TextStyle,
)
from .search import search_numeric_prefixed_pdfs, search_pdfs

# Core functionality
from .slides_to_text import extract_text_from_pdf, process_directory

__version__ = version("pdflex")

__all__ = [
    # Patterns
    "BaseExtractor",
    "ExtractionError",
    "ExtractionPattern",
    # Extractors
    "PDFDataExtractor",
    # Modifiers
    "PDFTextReplacer",
    # Exceptions
    "PDFlexError",
    "RegexExtractor",
    "ReplacementError",
    "ReplacementRule",
    "TextStyle",
    "ValidationError",
    # Converters
    "extract_text_from_pdf",
    # Mergers
    "merge_pdfs",
    "process_directory",
    "search_numeric_prefixed_pdfs",
    # Search
    "search_pdfs",
]


# Convenient function aliases
def extract_data(
    pdf_path: Union[str, Path], patterns: list[ExtractionPattern], **kwargs
) -> Dict[str, Any]:
    r"""
    Extract structured data from a PDF using patterns.

    Args:
        pdf_path: Path to the PDF file
        patterns: List of extraction patterns
        **kwargs: Additional arguments for PDFDataExtractor

    Returns:
        Dict[str, Any]: Extracted data

    Example:
        >>> patterns = [
        ...     ExtractionPattern(name="invoice_number", pattern=r"Invoice #(\d+)", required=True)
        ... ]
        >>> data = extract_data("invoice.pdf", patterns)
    """
    extractor = PDFDataExtractor(patterns, **kwargs)
    return extractor.extract_from_file(pdf_path)


def replace_text(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    rules: list[ReplacementRule],
    **kwargs,
) -> None:
    """
    Replace text in a PDF file using replacement rules.

    Args:
        input_path: Input PDF path
        output_path: Output PDF path
        rules: List of replacement rules
        **kwargs: Additional arguments for PDFTextReplacer

    Example:
        >>> rules = [ReplacementRule(pattern=r"DRAFT", replacement="FINAL", font_size=16)]
        >>> replace_text("draft.pdf", "final.pdf", rules)
    """
    replacer = PDFTextReplacer(rules, **kwargs)
    replacer.replace_text(input_path, output_path)


__all__.extend([
    "extract_data",
    "replace_text",
])

import logging
import mimetypes
import warnings
from contextlib import contextmanager
from pathlib import Path
from typing import Union

import pymupdf as fitz
from pypdf import PdfReader

from pdflex.exceptions import PDFlexError
from pdflex.logger import Logger

_log = Logger(__name__)


@contextmanager
def suppress_pdf_warnings():
    """Context manager to temporarily suppress PDF-related warnings."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # Temporarily suppress PyMuPDF logging
        fitz_logger = logging.getLogger("fitz")
        original_level = fitz_logger.level
        fitz_logger.setLevel(logging.ERROR)
        try:
            yield
        finally:
            fitz_logger.setLevel(original_level)


def validate_pdf_file(file_path: Path, suppress_warnings: bool = True) -> bool:
    """
    Validate that the file is a valid PDF.

    Args:
        file_path (Path): Path to the PDF file
        suppress_warnings (bool): Whether to suppress PDF parsing warnings

    Returns:
        bool: True if valid PDF, False otherwise
    """
    if not file_path.exists():
        _log.error(f"File does not exist: {file_path}")
        return False

    if file_path.stat().st_size == 0:
        _log.error(f"File is empty: {file_path}")
        return False

    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type != "application/pdf":
        _log.error(f"File is not a PDF: {file_path} (mime type: {mime_type})")
        return False

    try:
        with suppress_pdf_warnings() if suppress_warnings else nullcontext():
            # Try PyMuPDF first
            doc = fitz.open(file_path)
            page_count = len(doc)
            doc.close()

            # Then try pypdf
            with open(file_path, "rb") as f:
                reader = PdfReader(f)
                if len(reader.pages) != page_count:
                    _log.warning(
                        f"Page count mismatch between libraries for {file_path}"
                    )

            return True

    except Exception as e:
        _log.error(f"Invalid PDF file {file_path}: {e!s}")
        return False


def extract_text_with_pymupdf(pdf_path: Path) -> list[str]:
    """Extract text using PyMuPDF (better for PowerPoint PDFs)."""
    text = []
    with suppress_pdf_warnings():
        doc = fitz.open(pdf_path)
        try:
            for page in doc:
                # Use 'text' mode instead of 'blocks' for PowerPoint PDFs
                page_text = page.get_text("text")
                if page_text.strip():
                    text.append(page_text)
        finally:
            doc.close()
    return text


def extract_text_with_pypdf(pdf_path: Path) -> list[str]:
    """Extract text using pypdf (fallback method)."""
    text = []
    with suppress_pdf_warnings(), open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text.strip():
                text.append(page_text)
    return text


def extract_text_from_pdf(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path] | None = None,
    method: str = "auto",
    suppress_warnings: bool = True,
) -> str:
    """
    Extract text from a PDF file and save it to a text file.

    Args:
        pdf_path (Union[str, Path]): Path to the PDF file
        output_path (Union[str, Path], optional): Path for the output text file.
            If not provided, will use the PDF filename with .txt extension
        method (str): Text extraction method ('auto', 'pymupdf', or 'pypdf')
        suppress_warnings (bool): Whether to suppress PDF parsing warnings

    Returns:
        str: Path to the output text file

    Raises:
        PDFlexError: If there's an error reading the PDF or writing the output
    """
    pdf_path = Path(pdf_path)

    if not validate_pdf_file(pdf_path, suppress_warnings):
        raise PDFlexError(f"Invalid or corrupted PDF file: {pdf_path}")

    if output_path is None:
        output_path = pdf_path.with_suffix(".txt")
    else:
        output_path = Path(output_path)

    try:
        _log.debug(f"Extracting text from {pdf_path} using method: {method}")
        text = []

        if method == "auto" or method == "pymupdf":
            try:
                text = extract_text_with_pymupdf(pdf_path)
                if not text and method == "auto":
                    _log.debug("PyMuPDF extraction failed, trying pypdf")
                    text = extract_text_with_pypdf(pdf_path)
            except Exception as e:
                if method == "pymupdf":
                    raise PDFlexError(f"PyMuPDF extraction failed: {e!s}")
                _log.debug(f"PyMuPDF extraction failed: {e!s}")
                text = extract_text_with_pypdf(pdf_path)
        elif method == "pypdf":
            text = extract_text_with_pypdf(pdf_path)
        else:
            raise PDFlexError(f"Unknown extraction method: {method}")

        if not text:
            raise PDFlexError("No text could be extracted from the PDF")

        # Join pages and write to file
        full_text = "\n".join(text)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(full_text, encoding="utf-8")

        return str(output_path)

    except Exception as e:
        raise PDFlexError(f"Error processing PDF {pdf_path}: {e!s}")


def process_directory(
    input_dir: Union[str, Path],
    output_dir: Union[str, Path] | None = None,
    method: str = "auto",
    suppress_warnings: bool = True,
) -> None:
    """
    Process all PDF files in a directory.

    Args:
        input_dir (Union[str, Path]): Directory containing PDF files
        output_dir (Union[str, Path], optional): Directory for output text files
        method (str): Text extraction method ('auto', 'pymupdf', or 'pypdf')
        suppress_warnings (bool): Whether to suppress PDF parsing warnings
    """
    input_path = Path(input_dir)

    if not input_path.is_dir():
        raise PDFlexError(f"Input directory not found: {input_path}")

    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

    for pdf_file in input_path.glob("*.pdf"):
        try:
            if output_dir:
                output_file = output_path / pdf_file.with_suffix(".txt").name
            else:
                output_file = None

            output = extract_text_from_pdf(
                pdf_file,
                output_file,
                method=method,
                suppress_warnings=suppress_warnings,
            )
            _log.info(f"Processed {pdf_file} -> {output}")

        except Exception as e:
            _log.error(f"Error processing {pdf_file}: {e!s}")

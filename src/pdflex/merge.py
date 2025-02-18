#!/usr/bin/env python3
"""
Module: merge
Description: Provides functionality to merge multiple PDF files into one PDF,
             inserting a blank separator page with the title of each document.
"""

import io
import logging
import os
import warnings
from pathlib import Path
from typing import List

from pypdf import PdfWriter
from reportlab.lib.pagesizes import landscape as rl_landscape

# Import ReportLab modules to generate the separator page.
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from pdflex.logger import Logger

warnings.filterwarnings("ignore", message="Multiple definitions in dictionary")
logging.getLogger("PyPDF2").setLevel(logging.ERROR)

_log = Logger(__name__)


def create_separator_page(title: str, landscape: bool = False) -> io.BytesIO:
    """
    Create a blank separator PDF page with the given title centered on the page.

    Underscores and hyphens in the title are replaced with spaces.
    The page orientation is set to landscape if the 'landscape' parameter is True.

    Parameters
    ----------
    title : str
        The title text to display on the separator page.
    landscape : bool, optional
        If True, set the page orientation to landscape. Default is False.

    Returns
    -------
    io.BytesIO
        A BytesIO object containing the generated PDF page.
    """
    # Clean the title by replacing underscores and hyphens with spaces.
    clean_title = title.replace("_", " ").replace("-", " ")

    packet = io.BytesIO()
    # Set page size based on orientation.
    page_size = rl_landscape(letter) if landscape else letter
    c = canvas.Canvas(packet, pagesize=page_size)
    width, height = page_size
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height / 2, clean_title)
    c.showPage()
    c.save()
    packet.seek(0)
    return packet


def merge_pdfs(pdf_paths: List[str], output_path: str, landscape: bool = False) -> None:
    """
    Merge multiple PDF files into a single PDF file in the given order, inserting
    a blank separator page with the title of each document before its contents.

    The separator page title is derived from the file name (without extension),
    with underscores and hyphens replaced by spaces. If 'landscape' is True,
    the separator page will be created in landscape orientation.

    Parameters
    ----------
    pdf_paths : list of str
        List of file paths to the PDF documents to be merged.
    output_path : str
        The output file path for the merged PDF.
    landscape : bool, optional
        If True, separator pages are created in landscape orientation. Default is False.

    Raises
    ------
    FileNotFoundError
        If any provided PDF file path does not exist.
    Exception
        If an error occurs during merging or writing the output PDF.
    """
    merger = PdfWriter()

    for pdf_path in pdf_paths:
        pdf_path = pdf_path.strip()
        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Create a separator page using the file stem (cleaned up title).
        title = Path(pdf_path).stem
        separator_pdf = create_separator_page(title, landscape=landscape)
        try:
            merger.append(separator_pdf)
        except Exception as e:
            merger.close()
            raise Exception(f"Error appending separator for {pdf_path}: {e}") from e

        try:
            merger.append(pdf_path)
        except Exception as e:
            merger.close()
            raise Exception(f"Error appending {pdf_path}: {e}") from e

    try:
        merger.write(output_path)
        _log.info(f"Successfully merged PDFs into {output_path}")
    except Exception as e:
        raise Exception(f"Error writing output PDF: {e}") from e
    finally:
        merger.close()

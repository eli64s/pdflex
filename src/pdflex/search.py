#!/usr/bin/env python3
"""
Module: search
Description: Provides functionality to search for PDF files based on naming criteria.
"""

import re
import warnings
from pathlib import Path
from typing import List

from pdflex.logger import Logger

warnings.filterwarnings("ignore", message="Multiple definitions in dictionary")
_log = Logger(__name__)


def search_pdfs(search_dir: str, prefix: str = "", suffix: str = "") -> List[str]:
    """
    Recursively search for PDF files in a directory whose filenames start with a given prefix
    and (optionally) end with a given suffix.

    Parameters
    ----------
    search_dir : str
        The directory to search within.
    prefix : str, optional
        The starting substring of the PDF filenames. Default is an empty string.
    suffix : str, optional
        The ending substring of the PDF filenames. Default is an empty string.

    Returns
    -------
    list of str
        Sorted list of PDF file paths that match the criteria.
    """
    base_path = Path(search_dir)
    if not base_path.is_dir():
        raise NotADirectoryError(f"{search_dir} is not a valid directory.")

    # Search recursively for PDF files and filter by prefix and suffix.
    pdf_files = []
    for file in base_path.rglob("*.pdf"):
        if file.name.startswith(prefix) and (
            file.name.endswith(suffix) if suffix else True
        ):
            _log.info(f"Found PDF file: {file}")
            pdf_files.append(str(file))

    # Sort files lexicographically.
    pdf_files.sort()
    return pdf_files


def search_numeric_prefixed_pdfs(search_dir: str) -> List[str]:
    """
    Recursively search for PDF files in the specified directory whose filenames begin with a numeric
    float prefix. The prefix is defined as one or more digits, a dot, one or more digits, followed by an underscore,
    for example, "1.2_Insertion_Sort.pdf".

    The files are returned in ascending order based on the numeric prefix.

    Parameters
    ----------
    search_dir : str
        The directory to search within.

    Returns
    -------
    list of str
        Sorted list of PDF file paths that have a numeric float prefix.
    """
    base_path = Path(search_dir)
    if not base_path.is_dir():
        raise NotADirectoryError(f"{search_dir} is not a valid directory.")

    # Regex to match filenames starting with a numeric float followed by an underscore.
    pattern = re.compile(r"^(\d+\.\d+)_")
    numbered_files = []
    for file in base_path.rglob("*.pdf"):
        match = pattern.match(file.name)
        if match:
            try:
                numeric_value = float(match.group(1))
            except ValueError:
                numeric_value = 0.0
            numbered_files.append((numeric_value, str(file)))
            _log.info(f"Found numeric file: {file} with prefix {numeric_value}")
    # Sort the list by the extracted numeric value.
    numbered_files.sort(key=lambda tup: tup[0])
    return [path for _, path in numbered_files]

"""
Tests for the PDF search functionality in the pdflex.search module.
"""

import os
from pathlib import Path

import pytest

from pdflex.search import search_numeric_prefixed_pdfs, search_pdfs


@pytest.fixture
def test_directory(tmp_path: Path):
    """Create a temporary directory structure with test PDF files.

    This fixture sets up a realistic directory structure containing various PDF files
    for testing different search scenarios.
    """
    # Create main directory structure
    pdf_dir = tmp_path / "test_pdfs"
    subdirs = ["lectures", "documents", "empty_dir"]

    for subdir in subdirs:
        (pdf_dir / subdir).mkdir(parents=True)

    # Create regular PDF files
    regular_files = ["report.pdf", "Chapter1.pdf", "Chapter2.pdf", "notes_final.pdf"]

    for filename in regular_files:
        (pdf_dir / "documents" / filename).touch()

    # Create lecture slides with numeric prefixes
    lecture_files = [
        "1.1_Introduction.pdf",
        "1.2_Basics.pdf",
        "2.1_Advanced.pdf",
        "2.2_Final.pdf",
    ]

    for filename in lecture_files:
        (pdf_dir / "lectures" / filename).touch()

    return pdf_dir


# Test Cases for search_pdfs


def test_search_pdfs_basic_functionality(test_directory: Path):
    """Test basic PDF file search functionality."""
    pdf_files = search_pdfs(str(test_directory))
    assert len(pdf_files) > 0
    assert all(file.endswith(".pdf") for file in pdf_files)
    assert all(os.path.exists(file) for file in pdf_files)


def test_search_pdfs_with_prefix(test_directory: Path):
    """Test PDF search with filename prefix filtering."""
    pdf_files = search_pdfs(str(test_directory), prefix="Chapter")
    assert len(pdf_files) == 2
    assert all("Chapter" in file for file in pdf_files)


def test_search_pdfs_with_suffix(test_directory: Path):
    """Test PDF search with filename suffix filtering."""
    pdf_files = search_pdfs(str(test_directory), suffix="_final.pdf")
    assert len(pdf_files) == 1
    assert pdf_files[0].endswith("_final.pdf")


def test_search_pdfs_empty_directory(test_directory: Path):
    """Test PDF search in an empty directory."""
    empty_dir = test_directory / "empty_dir"
    pdf_files = search_pdfs(str(empty_dir))
    assert len(pdf_files) == 0


def test_search_pdfs_invalid_directory():
    """Test PDF search with an invalid directory path."""
    with pytest.raises(NotADirectoryError):
        search_pdfs("/nonexistent/directory")


def test_search_pdfs_sorting(test_directory: Path):
    """Test that returned PDF files are properly sorted."""
    pdf_files = search_pdfs(str(test_directory))
    assert pdf_files == sorted(pdf_files)


# Test Cases for search_numeric_prefixed_pdfs


def test_search_numeric_prefixed_pdfs_basic(test_directory: Path):
    """Test basic numeric-prefixed PDF file search functionality."""
    lecture_dir = test_directory / "lectures"
    pdf_files = search_numeric_prefixed_pdfs(str(lecture_dir))
    assert len(pdf_files) == 4

    # Verify numeric sorting
    prefixes = [float(Path(file).name.split("_")[0]) for file in pdf_files]
    assert prefixes == sorted(prefixes)


def test_search_numeric_prefixed_pdfs_no_matches(test_directory: Path):
    """Test numeric-prefixed search in directory with no matching files."""
    docs_dir = test_directory / "documents"
    pdf_files = search_numeric_prefixed_pdfs(str(docs_dir))
    assert len(pdf_files) == 0


def test_search_numeric_prefixed_pdfs_invalid_directory():
    """Test numeric-prefixed search with an invalid directory path."""
    with pytest.raises(NotADirectoryError):
        search_numeric_prefixed_pdfs("/nonexistent/directory")


def test_search_numeric_prefixed_pdfs_mixed_content(tmp_path: Path):
    """Test numeric-prefixed search with mixed valid and invalid filenames."""
    # Create test files with various naming patterns
    test_files = [
        "1.1_valid.pdf",  # Valid
        "1.2_also_valid.pdf",  # Valid
        "1.x_invalid.pdf",  # Invalid format
        "not_numeric.pdf",  # No numeric prefix
        "2.1.pdf",  # Missing underscore
    ]

    for filename in test_files:
        (tmp_path / filename).touch()

    pdf_files = search_numeric_prefixed_pdfs(str(tmp_path))
    assert len(pdf_files) == 2  # Should only find the valid numeric-prefixed files

    # Verify correct files were found
    filenames = [Path(file).name for file in pdf_files]
    assert "1.1_valid.pdf" in filenames
    assert "1.2_also_valid.pdf" in filenames


def test_search_numeric_prefixed_pdfs_sorting_precision(tmp_path: Path):
    """Test precise numeric sorting of PDF files with float prefixes."""
    test_files = ["1.11_test.pdf", "1.2_test.pdf", "1.02_test.pdf", "2.1_test.pdf"]

    for filename in test_files:
        (tmp_path / filename).touch()

    pdf_files = search_numeric_prefixed_pdfs(str(tmp_path))

    # Extract and verify numeric ordering
    numbers = [float(Path(file).name.split("_")[0]) for file in pdf_files]
    assert numbers == [1.02, 1.11, 1.2, 2.1]

from pathlib import Path

import pytest

from pdflex.converters.slides_to_text import extract_text_from_pdf, process_directory
from pdflex.exceptions import PDFlexError

from ..utils import create_test_pdf


def test_extract_text_from_pdf(mock_pdf: Path, tmp_path: Path):
    """Test PDF text extraction with a real PDF file."""
    output_path = tmp_path / "output.txt"

    # Extract text from the mock PDF
    result = extract_text_from_pdf(mock_pdf, output_path)

    # Verify the output file exists
    assert Path(result).exists()

    # Verify the content
    with open(result, encoding="utf-8") as f:
        content = f.read()
        assert "Test PDF Content" in content


def test_process_directory(tmp_path: Path):
    """Test processing multiple PDFs in a directory."""
    # Create test directory structure
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"

    # Create multiple test PDFs
    pdf_files = ["test1.pdf", "test2.pdf", "test3.pdf"]
    for pdf_file in pdf_files:
        pdf_path = input_dir / pdf_file
        create_test_pdf(pdf_path)

    # Process the directory
    process_directory(input_dir, output_dir)

    # Verify output files
    assert output_dir.exists()
    for pdf_file in pdf_files:
        txt_file = output_dir / pdf_file.replace(".pdf", ".txt")
        assert txt_file.exists()
        with open(txt_file, encoding="utf-8") as f:
            content = f.read()
            assert "Test PDF Content" in content


def test_extract_text_from_pdf_invalid_file(tmp_path: Path):
    """Test handling of non-existent PDF file."""
    pdf_path = tmp_path / "nonexistent.pdf"
    output_path = tmp_path / "output.txt"

    with pytest.raises(PDFlexError) as e:
        extract_text_from_pdf(pdf_path, output_path)
    assert isinstance(e.value, PDFlexError)


def test_process_directory_empty(tmp_path: Path):
    """Test processing an empty directory."""
    input_dir = tmp_path / "empty"
    input_dir.mkdir()
    output_dir = tmp_path / "output"

    process_directory(input_dir, output_dir)
    assert output_dir.exists()
    assert len(list(output_dir.glob("*.txt"))) == 0

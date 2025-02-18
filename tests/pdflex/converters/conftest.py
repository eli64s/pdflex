import random
from pathlib import Path
from typing import Tuple

import pytest
from reportlab.lib.colors import black, blue, red
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


class MathProblemGenerator:
    """Generates random math problems for test data."""

    @staticmethod
    def generate_addition() -> Tuple[str, str]:
        a = random.randint(10, 100)
        b = random.randint(10, 100)
        return f"{a} + {b} = ?", f"{a + b}"

    @staticmethod
    def generate_multiplication() -> Tuple[str, str]:
        a = random.randint(2, 20)
        b = random.randint(2, 20)
        return f"{a} × {b} = ?", f"{a * b}"

    @staticmethod
    def generate_division() -> Tuple[str, str]:
        b = random.randint(1, 12)
        a = b * random.randint(1, 12)
        return f"{a} ÷ {b} = ?", f"{a // b}"

    @staticmethod
    def generate_square_root() -> Tuple[str, str]:
        n = random.randint(2, 12)
        square = n * n
        return f"√{square} = ?", f"{n}"


def create_test_pdf(
    output_path: Path,
    num_slides: int = 3,
    problems_per_slide: int = 3,
    page_size: Tuple[float, float] = letter,
    corrupt: bool = False,
) -> Path:
    """Create a test PDF with math problems."""
    c = canvas.Canvas(str(output_path), pagesize=page_size)

    generators = [
        MathProblemGenerator.generate_addition,
        MathProblemGenerator.generate_multiplication,
        MathProblemGenerator.generate_division,
        MathProblemGenerator.generate_square_root,
    ]

    for slide in range(num_slides):
        # Draw slide title
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(blue)
        c.drawString(inch, 10 * inch, f"Test Slide {slide + 1}")

        # Generate and draw problems
        c.setFont("Helvetica", 16)
        c.setFillColor(black)
        y_position = 8.5 * inch

        for i in range(problems_per_slide):
            generator = random.choice(generators)
            problem, solution = generator()

            c.drawString(inch, y_position, f"{i + 1}. {problem}")
            c.setFillColor(red)
            c.drawString(5 * inch, y_position, f"Answer: {solution}")
            c.setFillColor(black)

            y_position -= inch

        c.showPage()

    c.save()

    if corrupt:
        # Simulate PDF corruption by truncating the file
        with open(output_path, "ab") as f:
            f.truncate(f.tell() // 2)

    return output_path


@pytest.fixture
def pdf_test_data(tmp_path: Path):
    """
    Fixture providing methods to generate test PDF files.

    Returns a factory function that can create test PDFs with various configurations.
    """

    def _create_test_pdf(
        filename: str = "test.pdf",
        num_slides: int = 3,
        problems_per_slide: int = 3,
        corrupt: bool = False,
    ) -> Path:
        """
        Create a test PDF file.

        Args:
            filename (str): Name of the output file
            num_slides (int): Number of slides to generate
            problems_per_slide (int): Problems per slide
            corrupt (bool): Whether to corrupt the PDF

        Returns:
            Path: Path to the generated PDF file
        """
        output_path = tmp_path / filename
        return create_test_pdf(
            output_path,
            num_slides=num_slides,
            problems_per_slide=problems_per_slide,
            corrupt=corrupt,
        )

    return _create_test_pdf


@pytest.fixture
def test_pdf_single(pdf_test_data) -> Path:
    """Fixture that provides a single-slide test PDF."""
    return pdf_test_data("single.pdf", num_slides=1)


@pytest.fixture
def test_pdf_multi(pdf_test_data) -> Path:
    """Fixture that provides a multi-slide test PDF."""
    return pdf_test_data("multi.pdf", num_slides=5)


@pytest.fixture
def test_pdf_corrupted(pdf_test_data) -> Path:
    """Fixture that provides a corrupted test PDF."""
    return pdf_test_data("corrupted.pdf", corrupt=True)


@pytest.fixture
def test_pdf_dir(pdf_test_data, tmp_path: Path) -> Path:
    """
    Fixture that provides a directory with multiple test PDFs.

    Creates:
    - Normal PDFs with varying sizes
    - A corrupted PDF
    - A non-PDF file
    """
    pdf_dir = tmp_path / "test_pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)

    # Create various test PDFs
    pdf_test_data("sample1.pdf", num_slides=2, problems_per_slide=3)
    pdf_test_data("sample2.pdf", num_slides=3, problems_per_slide=4)
    pdf_test_data("sample3.pdf", num_slides=1, problems_per_slide=2)
    pdf_test_data("corrupted.pdf", num_slides=1, corrupt=True)

    # Create a non-PDF file
    (pdf_dir / "not_a_pdf.txt").write_text("This is not a PDF file")

    return pdf_dir


# Example test using the fixtures
def test_pdf_extraction_example(
    test_pdf_single, test_pdf_multi, test_pdf_corrupted, test_pdf_dir
):
    """Example showing how to use the PDF test fixtures."""
    # Test single PDF extraction
    assert test_pdf_single.exists()
    assert test_pdf_single.suffix == ".pdf"

    # Test multi-slide PDF extraction
    assert test_pdf_multi.exists()
    assert test_pdf_multi.suffix == ".pdf"

    # Test corrupted PDF handling
    assert test_pdf_corrupted.exists()

    # Test directory processing
    assert test_pdf_dir.is_dir()
    assert len(list(test_pdf_dir.glob("*.pdf"))) >= 4  # At least 4 PDF files
    assert (test_pdf_dir / "not_a_pdf.txt").exists()


output_path = Path.cwd() / "data/slide-deck-math.pdf"
create_test_pdf(
    output_path=output_path,
    num_slides=30,
    problems_per_slide=5,
)

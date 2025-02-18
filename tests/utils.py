from pathlib import Path

from reportlab.pdfgen import canvas


def create_test_pdf(path: Path) -> None:
    """Create a simple PDF file for testing."""
    c = canvas.Canvas(str(path))
    c.drawString(100, 750, "Test PDF Content")
    c.showPage()
    c.save()

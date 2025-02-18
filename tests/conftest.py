# from pathlib import Path

# import pytest

# from pdflex.extractors.patterns import ExtractionPattern
# from pdflex.modifiers.text_replacement import ReplacementRule

# from .utils import create_test_pdf

# # -- Mock Data ---------


# @pytest.fixture
# def mock_pdf(tmp_path: Path) -> Path:
#     """Fixture to create a temporary PDF file."""
#     pdf_path = tmp_path / "test.pdf"
#     create_test_pdf(pdf_path)
#     return pdf_path


# # -- Extractors ---------


# @pytest.fixture
# def sample_patterns() -> list[ExtractionPattern]:
#     return [
#         ExtractionPattern(
#             name="name", pattern=r"Name:\s*(.+)", type="string", required=True
#         ),
#         ExtractionPattern(
#             name="amount",
#             pattern=r"\$\s*([\d,]+\.?\d*)",
#             type="currency",
#             multiple=True,
#         ),
#     ]


# # -- Modifiers ---------


# @pytest.fixture
# def sample_rules() -> list[ReplacementRule]:
#     return [
#         ReplacementRule(
#             pattern=r"(Test\s\d+)", replacement="Replacement", coordinates=(100, 100)
#         )
#     ]

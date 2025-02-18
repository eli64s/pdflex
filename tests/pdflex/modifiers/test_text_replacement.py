from pathlib import Path

import pytest

from pdflex.exceptions import PDFlexValidationError
from pdflex.modifiers.text_replacement import (
    PDFTextReplacer,
    ReplacementRule,
)


def test_text_replacement(tmp_path: Path, sample_rules: list[ReplacementRule]):
    # Create test PDF with known content
    input_pdf = tmp_path / "test.pdf"
    output_pdf = tmp_path / "output.pdf"

    # TODO: Add test PDF creation

    replacer = PDFTextReplacer(sample_rules)
    replacer.replace_text(input_pdf, output_pdf)

    assert output_pdf.exists()


def test_invalid_pattern():
    with pytest.raises(PDFlexValidationError) as e:
        PDFTextReplacer([
            ReplacementRule(
                pattern="[",  # Invalid regex
                replacement="test",
            )
        ])
    assert isinstance(e.value, PDFlexValidationError)

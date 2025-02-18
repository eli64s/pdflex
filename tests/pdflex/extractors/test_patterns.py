import pytest

from pdflex.exceptions import ExtractionError, ValidationError
from pdflex.extractors.patterns import (
    ExtractionPattern,
    RegexExtractor,
)


def test_regex_extractor(sample_patterns: list[ExtractionPattern]):
    extractor = RegexExtractor(sample_patterns)
    text = "Name: John Doe\nAmount: $100.50\nSecond Amount: $200.75"

    result = extractor.extract(text)
    assert result["name"] == "John Doe"
    assert result["amount"] == [100.50, 200.75]


def test_required_pattern_missing(sample_patterns: list[ExtractionPattern]):
    extractor = RegexExtractor(sample_patterns)
    text = "Amount: $100.50"  # Missing required name

    with pytest.raises(ExtractionError):
        extractor.extract(text)


def test_invalid_pattern():
    with pytest.raises(ValidationError):
        RegexExtractor([
            ExtractionPattern(
                name="invalid",
                pattern="[",  # Invalid regex
                type="string",
            )
        ])

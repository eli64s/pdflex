"""Custom exceptions for the pdflex package."""

# -- pdflex --------------


class PDFlexError(Exception): ...


class PDFlexIOError(PDFlexError): ...


class PDFlexValidationError(PDFlexError): ...


# -- pdflex.converters ---------


class ConversionError(PDFlexError): ...


# -- pdflex.extractors ---------


class ExtractionError(PDFlexError): ...


# -- pdflex.modifiers ---------


class ReplacementError(PDFlexError): ...


class ValidationError(PDFlexError): ...

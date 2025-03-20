import mimetypes
import warnings
from pathlib import Path
from typing import List, Union

from pypdf import PdfReader

from pdflex.exceptions import PDFlexError
from pdflex.logger import Logger

_log = Logger(__name__)


def convert_pdf_to_text(pdf_path: Union[str, Path], masking_words: List[str] = None) -> str:
    """Converts a PDF to text, removing blank lines and masking words."""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"File does not exist: {pdf_path}")

    mime_type, _ = mimetypes.guess_type(str(pdf_path))
    if mime_type != "application/pdf":
        raise ValueError(f"File is not a PDF: {pdf_path} (mime type: {mime_type})")

    try:
        text = ""
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            with open(pdf_path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    _log.debug(f"Extracted text from page {page.number}: {page_text}")
                    if page_text.strip():  # Skip blank lines
                        text += page_text + " "

        # Masking Words
        if masking_words:
            for word in masking_words:
                text = text.replace(word, "[MASKED]")

        if not text.strip():
            raise PDFlexError(f"No text could be extracted from {pdf_path}")

        return text.strip()

    except Exception as e:
        raise PDFlexError(f"Error converting PDF to text: {e!s}")


def write_text_to_file(text: str, output_file: Path) -> None:
    """Writes text to a file, ignoring potential errors."""
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(text, encoding="utf-8")
    except Exception as e:
        _log.warning(f"Error writing to file {output_file}: {e!s}")

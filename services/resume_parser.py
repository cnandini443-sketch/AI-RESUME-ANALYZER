
import re
from pathlib import Path

from PyPDF2 import PdfReader
from docx import Document


def _clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n +", "\n", text)
    text = re.sub(r" +\n", "\n", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\uFFFD|\x00", "", text)
    return text.strip()


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        if not path.exists() or path.stat().st_size == 0:
            raise ValueError("Uploaded PDF is empty or missing.")
        reader = PdfReader(str(path))
        pages = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            pages.append(page_text)
        return _clean_text("\n".join(pages))

    if suffix == ".docx":
        if not path.exists() or path.stat().st_size == 0:
            raise ValueError("Uploaded DOCX file is empty or missing.")
        document = Document(str(path))
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        return _clean_text("\n".join(paragraphs))

    raise ValueError("Unsupported file type.")

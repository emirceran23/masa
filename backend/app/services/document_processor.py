"""Document processor — PDF / DOCX → plain text conversion."""

from __future__ import annotations

import io
import fitz  # PyMuPDF
from docx import Document as DocxDocument

from app.services.ocr_service import ocr_image_bytes


def pdf_to_text(data: bytes) -> str:
    """Extract text from a PDF file. Falls back to OCR for scanned pages."""
    doc = fitz.open(stream=data, filetype="pdf")
    pages: list[str] = []

    for page in doc:
        text = page.get_text("text")
        if text.strip():
            pages.append(text)
        else:
            # Page has no selectable text → try OCR
            pix = page.get_pixmap(dpi=300)
            img_bytes = pix.tobytes("png")
            ocr_text = ocr_image_bytes(img_bytes)
            if ocr_text.strip():
                pages.append(ocr_text)

    doc.close()
    return "\n\n".join(pages)


def docx_to_text(data: bytes) -> str:
    """Extract text from a DOCX file."""
    doc = DocxDocument(io.BytesIO(data))
    paragraphs: list[str] = []
    for para in doc.paragraphs:
        if para.text.strip():
            paragraphs.append(para.text)
    return "\n\n".join(paragraphs)


def extract_text(data: bytes, file_format: str) -> str:
    """Unified entry point — dispatches by format."""
    fmt = file_format.lower().strip(".")
    if fmt == "pdf":
        return pdf_to_text(data)
    elif fmt in ("docx", "doc"):
        return docx_to_text(data)
    else:
        raise ValueError(f"Desteklenmeyen format: {file_format}")

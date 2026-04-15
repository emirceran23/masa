"""OCR service — Tesseract wrapper for scanned documents."""

from __future__ import annotations

import io
from PIL import Image
import pytesseract


def ocr_image_bytes(img_bytes: bytes, lang: str = "tur") -> str:
    """Run Tesseract OCR on raw image bytes. Default language: Turkish."""
    image = Image.open(io.BytesIO(img_bytes))
    text: str = pytesseract.image_to_string(image, lang=lang)
    return text

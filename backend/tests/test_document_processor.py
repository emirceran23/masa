"""Unit tests for document processing (text extraction)."""

import pytest

from app.services.document_processor import extract_text


@pytest.mark.asyncio
class TestExtractText:
    async def test_unsupported_format_raises(self):
        with pytest.raises(ValueError, match="Desteklenmeyen"):
            await extract_text(b"dummy", "file.txt")

    async def test_pdf_extraction_returns_string(self, tmp_path):
        """Smoke test — creates a minimal dummy PDF to verify the pipeline."""
        # Create minimal PDF bytes (simplest valid PDF)
        pdf_bytes = (
            b"%PDF-1.0\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj "
            b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj "
            b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R"
            b"/Resources<<>>>>endobj\n"
            b"xref\n0 4\n"
            b"0000000000 65535 f \n"
            b"0000000009 00000 n \n"
            b"0000000058 00000 n \n"
            b"0000000115 00000 n \n"
            b"trailer<</Size 4/Root 1 0 R>>\nstartxref\n210\n%%EOF"
        )
        result = await extract_text(pdf_bytes, "test.pdf")
        assert isinstance(result, str)

    async def test_docx_extraction_returns_string(self):
        """Smoke test with docx — requires python-docx."""
        from docx import Document
        import io

        doc = Document()
        doc.add_paragraph("Bu bir test cümlesidir.")
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        result = await extract_text(buffer.read(), "test.docx")
        assert "test cümlesidir" in result

"""
Doküman Parser Servisi — PDF ve DOCX dosyalarından metin çıkarma.
"""

from pathlib import Path


class DocumentParser:
    """PDF ve DOCX dosyalarını metne dönüştüren servis."""

    @staticmethod
    async def parse_pdf(file_path: Path) -> str:
        """PDF dosyasından metin çıkar (PyMuPDF)."""
        import fitz  # PyMuPDF

        text_parts: list[str] = []
        with fitz.open(str(file_path)) as doc:
            for page in doc:
                text_parts.append(page.get_text())
        return "\n".join(text_parts)

    @staticmethod
    async def parse_docx(file_path: Path) -> str:
        """DOCX dosyasından metin çıkar (python-docx)."""
        from docx import Document

        doc = Document(str(file_path))
        return "\n".join(para.text for para in doc.paragraphs if para.text.strip())

    async def parse(self, file_path: Path) -> str:
        """Dosya uzantısına göre uygun parser'ı seç ve metni çıkar."""
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            return await self.parse_pdf(file_path)
        elif suffix == ".docx":
            return await self.parse_docx(file_path)
        else:
            raise ValueError(f"Desteklenmeyen dosya formatı: {suffix}")

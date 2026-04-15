"""Unit tests for validators."""

import pytest

from app.utils.validators import (
    validate_email,
    validate_file_extension,
    validate_file_size,
    validate_password_strength,
)


class TestValidateFileExtension:
    def test_valid_pdf(self):
        assert validate_file_extension("contract.pdf") == "pdf"

    def test_valid_docx(self):
        assert validate_file_extension("contract.docx") == "docx"

    def test_invalid_extension(self):
        with pytest.raises(ValueError, match="Desteklenmeyen"):
            validate_file_extension("image.png")

    def test_no_extension(self):
        with pytest.raises(ValueError, match="Desteklenmeyen"):
            validate_file_extension("noextension")


class TestValidateFileSize:
    def test_within_limit(self):
        validate_file_size(5 * 1024 * 1024)  # 5 MB — OK

    def test_exceeds_limit(self):
        with pytest.raises(ValueError, match="maksimum"):
            validate_file_size(15 * 1024 * 1024)  # 15 MB — exceeds


class TestValidateEmail:
    def test_valid_email(self):
        assert validate_email("User@Example.COM") == "user@example.com"

    def test_invalid_email(self):
        with pytest.raises(ValueError, match="Geçersiz"):
            validate_email("not-an-email")


class TestValidatePasswordStrength:
    def test_strong_password(self):
        validate_password_strength("StrongP@ss123!")  # OK

    def test_too_short(self):
        with pytest.raises(ValueError, match="12 karakter"):
            validate_password_strength("Sh0rt!")

    def test_no_uppercase(self):
        with pytest.raises(ValueError, match="büyük harf"):
            validate_password_strength("alllowercase1!")

    def test_no_digit(self):
        with pytest.raises(ValueError, match="rakam"):
            validate_password_strength("NoDigitHere!@#abc")

    def test_no_special(self):
        with pytest.raises(ValueError, match="özel karakter"):
            validate_password_strength("NoSpecial12345AB")

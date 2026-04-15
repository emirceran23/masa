"""Input validation helpers."""

import re

ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def validate_file_extension(filename: str) -> str:
    """Return the lowercase extension if valid, else raise ValueError."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Desteklenmeyen dosya formatı: .{ext}")
    return ext


def validate_file_size(size: int) -> None:
    """Raise ValueError if file exceeds maximum allowed size."""
    if size > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"Dosya boyutu {size / (1024*1024):.1f} MB, "
            f"maksimum {MAX_FILE_SIZE_BYTES / (1024*1024):.0f} MB"
        )


def validate_email(email: str) -> str:
    """Basic e-mail format validation."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        raise ValueError("Geçersiz e-posta adresi")
    return email.lower().strip()


def validate_password_strength(password: str) -> None:
    """Enforce password policy (min 12 chars, mixed case, digit, special)."""
    errors: list[str] = []
    if len(password) < 12:
        errors.append("En az 12 karakter olmalıdır")
    if not re.search(r"[A-Z]", password):
        errors.append("En az bir büyük harf içermelidir")
    if not re.search(r"[a-z]", password):
        errors.append("En az bir küçük harf içermelidir")
    if not re.search(r"\d", password):
        errors.append("En az bir rakam içermelidir")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("En az bir özel karakter içermelidir")
    if errors:
        raise ValueError("; ".join(errors))

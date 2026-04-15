"""MinIO object-storage client wrapper."""

from __future__ import annotations

import io
from minio import Minio
from minio.error import S3Error

from app.config import settings


def _get_client() -> Minio:
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
    )


def ensure_bucket() -> None:
    """Create the default bucket if it doesn't exist (called on startup)."""
    client = _get_client()
    if not client.bucket_exists(settings.MINIO_BUCKET):
        client.make_bucket(settings.MINIO_BUCKET)


def upload_file(object_name: str, data: bytes, content_type: str) -> str:
    """Upload bytes to MinIO. Returns the object path."""
    client = _get_client()
    client.put_object(
        settings.MINIO_BUCKET,
        object_name,
        io.BytesIO(data),
        length=len(data),
        content_type=content_type,
    )
    return f"{settings.MINIO_BUCKET}/{object_name}"


def download_file(object_name: str) -> bytes:
    """Download an object from MinIO and return raw bytes."""
    client = _get_client()
    response = client.get_object(settings.MINIO_BUCKET, object_name)
    try:
        return response.read()
    finally:
        response.close()
        response.release_conn()


def delete_file(object_name: str) -> None:
    client = _get_client()
    client.remove_object(settings.MINIO_BUCKET, object_name)

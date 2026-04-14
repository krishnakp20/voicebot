import os
from pathlib import Path

import boto3

from app.core.config import settings


def ensure_recordings_dir() -> Path:
    path = Path(settings.recordings_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def local_recording_path(file_name: str) -> str:
    base = ensure_recordings_dir()
    return str(base / file_name)


def upload_to_s3(local_path: str, key: str) -> str:
    if not settings.s3_bucket:
        return local_path

    client = boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint_url or None,
        region_name=settings.s3_region,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
    )
    client.upload_file(local_path, settings.s3_bucket, key)
    endpoint = settings.s3_endpoint_url.rstrip("/") if settings.s3_endpoint_url else ""
    if endpoint:
        return f"{endpoint}/{settings.s3_bucket}/{key}"
    return f"s3://{settings.s3_bucket}/{key}"


def stream_recording_target(path_or_url: str) -> str:
    if path_or_url.startswith("s3://") or path_or_url.startswith("http"):
        return path_or_url
    return os.path.abspath(path_or_url)

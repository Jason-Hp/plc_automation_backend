from __future__ import annotations

from pathlib import Path
from typing import Optional
import uuid

from app.config import settings

import boto3
from botocore.exceptions import BotoCoreError, ClientError

# StorageService can save either locally or to AWS S3 depending on configuration.
# If S3 credentials and bucket are provided in settings, uploads go to S3 and the
# returned value is the public URL (CloudFront CDN URL if configured, otherwise S3 URL).
# Otherwise files are written to the local uploads directory and a Path is returned.

class StorageService:
    def __init__(self) -> None:
        self.use_s3 = False
        self.s3_client = None  # type: ignore
        self.s3_bucket = None  # type: ignore
        self.cloudfront_domain = None  # type: ignore

        if (
            settings.aws_s3_bucket
            and settings.aws_access_key_id
            and settings.aws_secret_access_key
        ):
            # initialise S3 client
            self.use_s3 = True
            self.s3_bucket = settings.aws_s3_bucket
            self.cloudfront_domain = settings.aws_cloudfront_domain
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region,
            )
        else:
            self.upload_dir = Path(settings.upload_dir)
            self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_upload(
        self,
        payload: bytes,
        original_filename: Optional[str] = None,
    ) -> str:
        """Store payload; return public link string.

        * When S3 is enabled and CloudFront is configured, the result is the CloudFront CDN URL.
        * When S3 is enabled but CloudFront is not configured, the result is the S3 HTTPS URL.
        * When falling back to local disk the result is the local path string.

        ``original_filename`` is only used to preserve an extension if present.
        """
        # generate a unique name (uuid4) and optionally keep extension
        ext = ""
        if original_filename:
            ext = Path(original_filename).suffix
        key = f"{uuid.uuid4()}{ext}"

        if self.use_s3:
            try:
                self.s3_client.put_object(Bucket=self.s3_bucket, Key=key, Body=payload)
            except (BotoCoreError, ClientError) as exc:
                # bubble up the exception to caller
                raise
            # Use CloudFront CDN URL if configured, otherwise use S3 URL
            if self.cloudfront_domain:
                return f"https://{self.cloudfront_domain}/{key}"
            else:
                region = settings.aws_region or "us-east-1"
                return f"https://{self.s3_bucket}.s3.{region}.amazonaws.com/{key}"
        else:
            destination = self.upload_dir / key
            destination.write_bytes(payload)
            return str(destination)

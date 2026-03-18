from __future__ import annotations

from typing import Optional
import uuid

from app.config import settings
from app.services.log_service import LogService
from app.dependencies import email_service

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class StorageService:
    def __init__(self) -> None:
        self.s3_client = None  
        self.cloudfront_domain = None  

        if (
            settings.aws_access_key_id
            and settings.aws_secret_access_key
        ):
            # initialise S3 client
            self.cloudfront_domain = settings.aws_cloudfront_domain
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region,
            )
        else:
            LogService.ERROR.log("AWS S3 credentials not configured. StorageService will not be functional.", level="ERROR")
            email_service.send(
                subject="URGENT!!! AWS S3 Configuration Missing",
                body="AWS S3 credentials are not configured. StorageService will not be functional. Please check the logs for details.",
                html_body=None,
                to_addrs=[settings.admin_email]
            )
            raise NotImplementedError("Please configure AWS S3 credentials and bucket to enable storage.")

    def get_object_url(self, bucket: str, key: str) -> str:

        try:
            # Check if object exists first
            self.s3_client.head_object(Bucket=bucket, Key=key)

            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=900  # 15 minutes expiration
            )
            return presigned_url
        except Exception as exc:
            LogService.ERROR.log(f"Failed to generate presigned URL: {str(exc)}", level="ERROR")
            raise exc
    
    def save_upload_private(
        self,
        bucket: str,
        payload: bytes,
        original_filename: Optional[str] = None,
    ):
        # For private storage, mainly for logs for now
        key = original_filename or f"{uuid.uuid4()}"

        try:
            self.s3_client.put_object(Bucket=bucket, Key=key, Body=payload)
        except (BotoCoreError, ClientError) as exc:
            LogService.ERROR.log(f"Failed to upload log to S3: {str(exc)}", level="ERROR")
            email_service.send(
                subject="URGENT!!! Failed to Upload Logs to S3",
                body=f"An error occurred while uploading logs to S3: {str(exc)}. Please check the logs for details.",
                html_body=None,
                to_addrs=[settings.admin_email]
            )
            raise exc


    def save_upload_public(
        self,
        bucket: str,
        payload: bytes,
        original_filename: Optional[str] = None,
    ) -> str:

        key = f"{uuid.uuid4()}-{original_filename or 'DEFAULT'}"

        try:
            self.s3_client.put_object(Bucket=bucket, Key=key, Body=payload)
        except (BotoCoreError, ClientError) as exc:
            LogService.ERROR.log(f"Failed to upload file to S3: {str(exc)}", level="ERROR")
            raise exc

        # Use CloudFront CDN URL if configured, otherwise use S3 URL; THIS IS IMPORTANT TO REDUCE COSTS AND IMPROVE PERFORMANCE
        if self.cloudfront_domain:
            return f"https://{self.cloudfront_domain}/{key}"
        else:
            region = settings.aws_region or "us-east-1"
            return f"https://{bucket}.s3.{region}.amazonaws.com/{key}"


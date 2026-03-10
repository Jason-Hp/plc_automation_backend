from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional

# Get project root directory
CONFIG_DIR = Path(__file__).parent  # app/
PROJECT_ROOT = CONFIG_DIR.parent     # plc_automation_backend/
LOG_DIR = PROJECT_ROOT / "logs"
UPLOAD_DIR = PROJECT_ROOT / "uploads"


class Settings(BaseSettings):
    app_name: str = "PLC Automation API"
    environment: str = "development"

    # comma-separated list of allowed origins for CORS (NOT CHANGABLE IN ADMIN/RUNTIME,MUST RESTART SERVER)
    allowed_origins: str = "http://localhost:3000"

    # SMTP configuration TODO: update defaults
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from: str = "info@plcautomationgroup.com"

    # TODO: change to actual admin email
    admin_email: str = "sales@plcautomat.com"
    quote_and_enquiry_email: str = ""
    hr_email: str = "hr@plcautomat.com"

    # JWT configuration
    jwt_secret_key: str = "change_me_in_env"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 3

    # Admin is the only approver (REFACTOR ACCOUNTS TO BE STORED IN DB INSTEAD)
    admin_username: str = "admin"
    admin_password: str = "password"

    # Updater accounts
    updater_1_username: str = "updater1"
    updater_1_password: str = "password1"

    updater_2_username: str = "updater2"
    updater_2_password: str = "password2"

    upload_dir: str = str(UPLOAD_DIR)
    database_url: str = ""
    web_log_location: str = str(LOG_DIR / "web_logs")
    warn_log_location: str = str(LOG_DIR / "warn_logs")
    error_log_location: str = str(LOG_DIR / "error_logs")
    enquiry_log_location: str = str(LOG_DIR / "enquiry_logs")
    admin_log_location: str = str(LOG_DIR / "admin_logs")

    # AWS S3 configuration (if provided, StorageService will use S3)
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_s3_bucket: Optional[str] = None
    aws_region: Optional[str] = None
    aws_cloudfront_domain: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", case_sensitive=False)


settings = Settings()

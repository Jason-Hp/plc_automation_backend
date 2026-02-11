from enum import Enum
from app.services.email_service import EmailService
from app.config import settings


class AlertService(Enum):
    ERROR = "Error"

    def __init__(self, value: str) -> None:
        # Email service instance per enum member (created at import-time)
        self.email_svc = EmailService()
        self.alert_type = value

    def send_alert(self, message: str) -> None:
        """Send an error alert email to admin."""
        subject = f"{self.alert_type} Alert Notification"
        to_addrs = [settings.admin_email]
        self.email_svc.send(
            subject,
            message,
            self.email_svc.smtp_from,
            to_addrs,
        )
    
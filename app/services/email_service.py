from __future__ import annotations

from email.message import EmailMessage
import smtplib
from typing import Iterable, Optional

from app.config import settings


class EmailService:
    def __init__(self) -> None:
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.smtp_from = settings.smtp_from

    def send(
        self,
        subject: str,
        body: str,
        html_body: Optional[str],
        to_addrs: Iterable[str],
        cc_addrs: Optional[Iterable[str]] = None,
        attachments: Optional[list[tuple[str, bytes, str]]] = None,
    ) -> None:
        if not self.smtp_host:
            raise RuntimeError("SMTP_HOST is not configured")

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self.smtp_from
        message["To"] = ", ".join(to_addrs)
        if cc_addrs:
            message["Cc"] = ", ".join(cc_addrs)

        message.set_content(body)

        if html_body:
            message.set_content("This is an HTML email. Please view in an HTML-compatible email viewer.")
            message.add_alternative(html_body, subtype="html")

        if attachments:
            for filename, payload, mime_type in attachments:
                maintype, subtype = mime_type.split("/", 1)
                message.add_attachment(payload, maintype=maintype, subtype=subtype, filename=filename)

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            if self.smtp_username and self.smtp_password:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
            server.send_message(message)

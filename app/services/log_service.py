from app.config import settings
from datetime import datetime
from enum import Enum
import os
import pytz

#TODO: Not a must, but consider either integrating with a actual logging library and moving
# this file to utils

class LogService(Enum):
    WEB = (settings.web_log_location, "web")
    ERROR = (settings.error_log_location, "error")
    ADMIN = (settings.admin_log_location, "admin")
    DEBUG = (settings.debug_log_location, "debug")

    def __init__(self, location: str, prefix: str):
        self.location = location
        self.prefix = prefix
        self.timezone = pytz.timezone(settings.timezone)

    def get_log_file(self) -> str:
        date_str = datetime.now(self.timezone).strftime("%Y-%m-%d")
        log_file = os.path.join(self.location, f"{self.prefix}_{date_str}.log")
        
        # Ensure the log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Create the log file if it does not exist
        if not os.path.isfile(log_file):
            open(log_file, 'a').close()

        return log_file

    def log(self, message: str, level: str = "INFO") -> None:
        
        level = level.upper()
        log_file = self.get_log_file()
        current_time = datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{level}] [{current_time}]: {message}\n"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(formatted_message)
        
        # Always log to web logs as well
        web_log_file = LogService.WEB.get_log_file()
        if log_file != web_log_file:
            with open(web_log_file, "a", encoding="utf-8") as f:
                f.write(formatted_message)
    
    def get_log_enum(log_type: str):
        for log_enum in LogService:
            if log_enum.prefix == log_type:
                return log_enum
        return LogService.WEB  # default to WEB if not found
    
    def get_all_enums():
        return [log_enum for log_enum in LogService]
    
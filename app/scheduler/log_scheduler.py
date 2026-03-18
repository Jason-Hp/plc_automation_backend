from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from app.config import settings
import os

from app.dependencies import storage_service, email_service
from app.services.log_service import LogService

def upload_logs_to_s3_and_clear_local():
    log_enums = LogService.get_all_enums()
    for log_enum in log_enums:
        
        # get previous day in SGT (UTC+8)
        timezone = pytz.timezone(settings.timezone)
        previous_day = datetime.now(timezone) - timedelta(days=1)
        date_str = previous_day.strftime("%Y-%m-%d")
        log_file = os.path.join(log_enum.location, f"{log_enum.prefix}_{date_str}.log")
        
        if os.path.isfile(log_file):
            with open(log_file, "rb") as f:
                payload = f.read()
                storage_service.save_upload_private(
                    bucket=settings.aws_s3_log_bucket,
                    payload=payload,
                    original_filename=f"{log_enum.prefix}_{date_str}.log"
                )

            # Clear local log after uploading
            os.remove(log_file)
            email_service.send(
                subject=f"Logs Uploaded: {log_enum.prefix}_{date_str}.log",
                body=f"The log file {log_enum.prefix}_{date_str}.log has been uploaded to S3 and cleared from local storage.",
                html_body=None,
                to_addrs=[settings.admin_email]
            )

# Start the background scheduler to run the log upload task daily
def start_log_scheduler():
    scheduled_worker = BackgroundScheduler()

    # 1 AM in SGT (UTC+8) is 5 PM UTC the previous day
    hour = 17  # 5 PM UTC

    # Scheduled at 1 AM SGT every day to upload logs to S3 and clear local logs
    trigger = CronTrigger(hour=hour, minute=0)  
    scheduled_worker.add_job(upload_logs_to_s3_and_clear_local, trigger)
    scheduled_worker.start()
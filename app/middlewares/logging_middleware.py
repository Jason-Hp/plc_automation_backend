import time
import traceback
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.services.log_service import LogService
from app.services.alert_service import AlertService


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> Response:
        
        # Log request
        start_time = time.time()
        request_body = await request.body()
        
        log_entry = {
            "event": "HTTP_REQUEST",
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else "unknown"
        }
        
        if request_body:
            try:
                log_entry["body"] = json.loads(request_body.decode())
            except Exception:
                log_entry["body"] = request_body.decode()[:100]  # First 100 chars
        
        LogService.WEB.log(json.dumps(log_entry))
        
        try:
            # Call the endpoint
            response = await call_next(request)
            
            # Log response
            duration = time.time() - start_time
            response_entry = {
                "event": "HTTP_RESPONSE",
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2)
            }
            LogService.WEB.log(json.dumps(response_entry))
            
            return response
        
        except Exception as e:
            # Log error with full stack trace
            duration = time.time() - start_time
            error_entry = {
                "event": "ERROR OCCURRED",
                "method": request.method,
                "path": request.url.path,
                "error": str(e),
                "error_type": type(e).__name__,
                "duration_ms": round(duration * 1000, 2),
                "stack_trace": traceback.format_exc(),
            }
            LogService.ERROR.log(json.dumps(error_entry), level="ERROR")
            LogService.WEB.log(json.dumps(error_entry), level="ERROR")
            AlertService.ERROR.send_alert(json.dumps(error_entry))

            raise

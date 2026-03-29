import time
import traceback
import json
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.services.log_service import LogService
from app.services.alert_service import AlertService


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> Response:
        
        # Log request
        start_time = time.time()
        request_body = await request.body()
        
        log_entry: dict[str, object] = {
            "event": "HTTP_REQUEST",
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else "unknown",
        }
        
        if request_body:
            content_type = request.headers.get("content-type", "")
            try:
                if "multipart/form-data" in content_type:
                    form = await request.form()
                    log_entry["body"] = {
                        key: (f"<file: {val.filename}>" if hasattr(val, "filename") else val)
                        for key, val in form.items()
                    }
                else:
                    parsed = json.loads(request_body.decode())
                    log_entry["body"] = self._redact_payload(parsed)
            except Exception:
                log_entry["body"] = request_body.decode("utf-8", errors="replace")[:100]
        
        LogService.WEB.log(json.dumps(log_entry))
        
        try:
            # Go next, basically call the endpoint
            response = await call_next(request)
            
            # Log response
            duration = time.time() - start_time
            response_entry: dict[str, object] = {
                "event": "HTTP_RESPONSE",
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2)
            }
            LogService.WEB.log(json.dumps(response_entry))
            
            return response
        
        except Exception as e:
            # Classify expected HTTP errors vs unhandled server errors.
            duration = time.time() - start_time
            is_http_exc = isinstance(e, HTTPException)
            status_code = e.status_code if is_http_exc else 500
            level = "WARNING" if is_http_exc and status_code < 500 else "ERROR"

            error_entry: dict[str, object] = {
                "event": "HTTP_EXCEPTION" if is_http_exc else "UNHANDLED_EXCEPTION",
                "method": request.method,
                "path": request.url.path,
                "error": str(e),
                "error_type": type(e).__name__,
                "status_code": status_code,
                "duration_ms": round(duration * 1000, 2),
                "stack_trace": traceback.format_exc(),
            }
            LogService.ERROR.log(json.dumps(error_entry), level=level)
            # Alert admin only for true server-side errors (5xx).
            if not is_http_exc or status_code >= 500:
                AlertService.ERROR.send_alert("Unhandled Exception", json.dumps(error_entry))

            raise

    @staticmethod
    def _redact_payload(payload: object) -> object:
        """Redact common secrets from logged request bodies."""
        secret_keys = {
            "password",
            "pass",
            "token",
            "access_token",
            "refresh_token",
            "authorization",
            "api_key",
            "apikey",
            "secret",
            "client_secret",
        }

        if isinstance(payload, dict):
            redacted: dict[object, object] = {}
            for k, v in payload.items():
                key_str = str(k).lower()
                if key_str in secret_keys:
                    redacted[k] = "***REDACTED***"
                else:
                    redacted[k] = LoggingMiddleware._redact_payload(v)
            return redacted
        if isinstance(payload, list):
            return [LoggingMiddleware._redact_payload(v) for v in payload]
        return payload

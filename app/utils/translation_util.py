from app.utils.context_util import lang_context
from app.services.alert_service import AlertService
from app.services.log_service import LogService

try:
    from googletrans import Translator  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    LogService.ERROR.log("googletrans library not installed. Translation functionality will be disabled.", level="ERROR")
    AlertService.ERROR.send_alert("Translation Service Unavailable", "googletrans library is not installed. Translation functionality will be disabled.")
    Translator = None


def translate_text(text: str) -> str:
    if not text:
        return text

    # If translator dependency is not installed or source and target lang are same,
    # return text unchanged.
    if Translator is None or lang_context.get() == "en":
        return text

    translator = Translator()
    try:
        translation = translator.translate(text, src='auto', dest=lang_context.get())
        return translation.text
    except Exception:
        LogService.ERROR.log(f"Translation failed for text: {text}", level="ERROR")
        AlertService.ERROR.send_alert("Translation Error", f"Failed to translate text: {text}")
        return text

from app.utils.context_util import lang_context
from app.services.log_service import LogService

try:
    from googletrans import Translator  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    LogService.DEBUG.log(
        "googletrans library not installed. Translation functionality will be disabled.",
        level="WARNING",
    )
    # Optional dependency; do not alert admin unless you explicitly want emails for missing deps.
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
        # Expected fallback: user still sees original text instead of an error.
        LogService.DEBUG.log(f"Translation failed; returning original text: {text}", level="WARNING")
        return text

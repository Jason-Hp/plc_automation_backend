from app.utils.context_util import lang_context
from app.services.log_service import LogService
from deep_translator import GoogleTranslator

def translate_text(text: str) -> str:
    if not text:
        return text

    if lang_context.get() == "en":
        return text
    
    try:
        return GoogleTranslator(source='auto', target=lang_context.get()).translate(text)
    except Exception:
        # Expected fallback: user still sees original text instead of an error.
        LogService.DEBUG.log(f"Translation failed to {lang_context.get()}; returning original text: {text}", level="WARNING")
        return text

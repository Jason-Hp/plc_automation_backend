from app.utils.context_util import lang_context

try:
    from googletrans import Translator  # type: ignore
except Exception:  # pragma: no cover - optional dependency
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
        return text

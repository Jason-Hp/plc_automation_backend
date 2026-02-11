from googletrans import Translator
from app.utils.context_util import lang_context

def translate_text(text: str) -> str:
    translator = Translator()
    translation = translator.translate(text, src_language='auto', dest_language=lang_context.get())
    return translation.text
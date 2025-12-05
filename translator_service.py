# src/translator_service.py

from googletrans import Translator


class TranslatorService:
    """
    Simple wrapper around googletrans Translator.
    - Auto-detects source language
    - Translates to target_lang (default: English)
    """

    def __init__(self, target_lang: str = "en"):
        self._translator = Translator()
        self.target_lang = target_lang

    def translate(self, text: str, src_lang: str = "auto") -> str:
        text = text.strip()
        if not text:
            return text

        try:
            result = self._translator.translate(text, src=src_lang, dest=self.target_lang)
            print(f"[Translate] '{text}' -> '{result.text}' (detected src={result.src})")
            return result.text
        except Exception as e:
            # If translation fails, show original text so UI still works
            print(f"[Translate] Error translating text: {e}")
            return text + "  [translation failed]"

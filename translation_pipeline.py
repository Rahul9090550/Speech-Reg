# src/translation_pipeline.py

from typing import Callable
from .translator_service import TranslatorService


def make_translating_callback(
    base_callback: Callable[[str], None],
    target_lang: str = "en",
):
    """
    Wraps an existing text callback so that:
      1. Raw recognized text is translated to `target_lang`
      2. Only the translated text is passed to base_callback

    Usage:
        translated_cb = make_translating_callback(text_state.add_line, "en")
        AudioListener(text_callback=translated_cb)
    """

    translator = TranslatorService(target_lang=target_lang)

    def callback(text: str):
        translated = translator.translate(text)
        base_callback(translated)

    return callback

# agent/translator.py
"""
Yojanasaathi Translator Agent
Provides English-to-Hindi translation for agent answers using googletrans.
Can be extended for other languages.
"""

from googletrans import Translator

def translate(text, lang="hindi"):
    """
    Translates given text from English to Hindi (or other supported languages).
    Args:
        text (str): Text to translate (English original).
        lang (str): Target language ('hindi' or language code).
    Returns:
        str: Translated text.
    """
    if not text or lang.lower() == "english":
        return text  # No translation needed

    translator = Translator()
    target = "hi" if lang.lower() == "hindi" else lang
    try:
        translated = translator.translate(text, dest=target)
        return translated.text
    except Exception as e:
        # Return English if translation fails
        print(f"Translation error: {e}")
        return text

# End of agent/translator.py

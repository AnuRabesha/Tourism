from flask import Blueprint, request, jsonify
import requests

language_bp = Blueprint("language", __name__)

# Uses MyMemory free translation API (no key needed for basic use)
TRANSLATE_URL = "https://api.mymemory.translated.net/get"

SUPPORTED_LANGUAGES = {
    "ta": "Tamil", "hi": "Hindi", "te": "Telugu",
    "ml": "Malayalam", "kn": "Kannada", "fr": "French",
    "de": "German", "ja": "Japanese", "zh": "Chinese",
    "es": "Spanish", "ar": "Arabic", "en": "English",
}

COMMON_PHRASES = {
    "ta": {"Hello": "வணக்கம்", "Thank you": "நன்றி", "Help": "உதவி", "Where is": "எங்கே உள்ளது"},
    "hi": {"Hello": "नमस्ते", "Thank you": "धन्यवाद", "Help": "मदद", "Where is": "कहाँ है"},
    "te": {"Hello": "నమస్కారం", "Thank you": "ధన్యవాదాలు", "Help": "సహాయం", "Where is": "ఎక్కడ ఉంది"},
}


@language_bp.route("/translate", methods=["POST"])
def translate():
    """Translate text. Body: {text, source_lang, target_lang}"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    text = data.get("text")
    source = data.get("source_lang", "en")
    target = data.get("target_lang", "ta")

    if not text:
        return jsonify({"error": "text is required"}), 400

    # Prevent same-language translation returning garbage
    if source == target:
        return jsonify({"original": text, "translated": text, "target_lang": target})

    try:
        resp = requests.get(TRANSLATE_URL, params={"q": text, "langpair": f"{source}|{target}"}, timeout=10)
        result = resp.json()
        translated = result.get("responseData", {}).get("translatedText", "")
        if not translated:
            return jsonify({"error": "Translation failed. Try again."}), 502
        return jsonify({"original": text, "translated": translated, "target_lang": target})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Translation service unavailable: {str(e)}"}), 503


@language_bp.route("/languages", methods=["GET"])
def supported_languages():
    """List all supported languages."""
    return jsonify(SUPPORTED_LANGUAGES)


@language_bp.route("/phrases/<lang_code>", methods=["GET"])
def common_phrases(lang_code):
    """Get common tourist phrases for a language."""
    phrases = COMMON_PHRASES.get(lang_code)
    if not phrases:
        return jsonify({"error": f"Phrases not available for '{lang_code}'"}), 404
    return jsonify({"language": SUPPORTED_LANGUAGES.get(lang_code, lang_code), "phrases": phrases})

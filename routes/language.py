from flask import Blueprint, request, jsonify
import requests

language_bp = Blueprint("language", __name__)

TRANSLATE_URL = "https://api.mymemory.translated.net/get"

SUPPORTED_LANGUAGES = {
    "ta": "Tamil", "hi": "Hindi", "te": "Telugu",
    "ml": "Malayalam", "kn": "Kannada", "fr": "French",
    "de": "German", "ja": "Japanese", "zh": "Chinese",
    "es": "Spanish", "ar": "Arabic", "en": "English",
}

# Accurate built-in translations for common tourist phrases
BUILTIN_TRANSLATIONS = {
    ("hello", "ta"): "வணக்கம்",
    ("thank you", "ta"): "நன்றி",
    ("help", "ta"): "உதவி",
    ("where is", "ta"): "எங்கே உள்ளது",
    ("how much", "ta"): "எவ்வளவு",
    ("water", "ta"): "தண்ணீர்",
    ("food", "ta"): "உணவு",
    ("hospital", "ta"): "மருத்துவமனை",
    ("police", "ta"): "காவல்துறை",
    ("hotel", "ta"): "ஹோட்டல்",
    ("toilet", "ta"): "கழிவறை",
    ("yes", "ta"): "ஆம்",
    ("no", "ta"): "இல்லை",
    ("good morning", "ta"): "காலை வணக்கம்",
    ("good night", "ta"): "இரவு வணக்கம்",
    ("sorry", "ta"): "மன்னிக்கவும்",
    ("please", "ta"): "தயவுசெய்து",

    ("hello", "hi"): "नमस्ते",
    ("thank you", "hi"): "धन्यवाद",
    ("help", "hi"): "मदद",
    ("where is", "hi"): "कहाँ है",
    ("how much", "hi"): "कितना",
    ("water", "hi"): "पानी",
    ("food", "hi"): "खाना",
    ("hospital", "hi"): "अस्पताल",
    ("police", "hi"): "पुलिस",
    ("hotel", "hi"): "होटल",
    ("toilet", "hi"): "शौचालय",
    ("yes", "hi"): "हाँ",
    ("no", "hi"): "नहीं",
    ("good morning", "hi"): "सुप्रभात",
    ("good night", "hi"): "शुभ रात्रि",
    ("sorry", "hi"): "माफ़ करें",
    ("please", "hi"): "कृपया",

    ("hello", "te"): "నమస్కారం",
    ("thank you", "te"): "ధన్యవాదాలు",
    ("help", "te"): "సహాయం",
    ("where is", "te"): "ఎక్కడ ఉంది",
    ("how much", "te"): "ఎంత",
    ("water", "te"): "నీరు",
    ("food", "te"): "ఆహారం",
    ("hospital", "te"): "ఆసుపత్రి",
    ("police", "te"): "పోలీసు",
    ("hotel", "te"): "హోటల్",
    ("yes", "te"): "అవును",
    ("no", "te"): "కాదు",
    ("good morning", "te"): "శుభోదయం",
    ("sorry", "te"): "క్షమించండి",
    ("please", "te"): "దయచేసి",

    ("hello", "ml"): "നമസ്കാരം",
    ("thank you", "ml"): "നന്ദി",
    ("help", "ml"): "സഹായം",
    ("where is", "ml"): "എവിടെ ആണ്",
    ("water", "ml"): "വെള്ളം",
    ("food", "ml"): "ഭക്ഷണം",
    ("yes", "ml"): "അതെ",
    ("no", "ml"): "ഇല്ല",
    ("good morning", "ml"): "സുപ്രഭാതം",
    ("sorry", "ml"): "ക്ഷമിക്കണം",

    ("hello", "kn"): "ನಮಸ್ಕಾರ",
    ("thank you", "kn"): "ಧನ್ಯವಾದಗಳು",
    ("help", "kn"): "ಸಹಾಯ",
    ("where is", "kn"): "ಎಲ್ಲಿದೆ",
    ("water", "kn"): "ನೀರು",
    ("food", "kn"): "ಆಹಾರ",
    ("yes", "kn"): "ಹೌದು",
    ("no", "kn"): "ಇಲ್ಲ",
    ("good morning", "kn"): "ಶುಭೋದಯ",
    ("sorry", "kn"): "ಕ್ಷಮಿಸಿ",
}

COMMON_PHRASES = {
    "ta": {
        "Hello": "வணக்கம்", "Thank you": "நன்றி",
        "Help": "உதவி", "Where is": "எங்கே உள்ளது",
        "How much": "எவ்வளவு", "Water": "தண்ணீர்",
        "Food": "உணவு", "Hospital": "மருத்துவமனை",
        "Police": "காவல்துறை", "Yes": "ஆம்",
        "No": "இல்லை", "Sorry": "மன்னிக்கவும்",
        "Please": "தயவுசெய்து", "Good morning": "காலை வணக்கம்",
    },
    "hi": {
        "Hello": "नमस्ते", "Thank you": "धन्यवाद",
        "Help": "मदद", "Where is": "कहाँ है",
        "How much": "कितना", "Water": "पानी",
        "Food": "खाना", "Hospital": "अस्पताल",
        "Police": "पुलिस", "Yes": "हाँ",
        "No": "नहीं", "Sorry": "माफ़ करें",
        "Please": "कृपया", "Good morning": "सुप्रभात",
    },
    "te": {
        "Hello": "నమస్కారం", "Thank you": "ధన్యవాదాలు",
        "Help": "సహాయం", "Where is": "ఎక్కడ ఉంది",
        "How much": "ఎంత", "Water": "నీరు",
        "Food": "ఆహారం", "Hospital": "ఆసుపత్రి",
        "Yes": "అవును", "No": "కాదు",
        "Sorry": "క్షమించండి", "Good morning": "శుభోదయం",
    },
    "ml": {
        "Hello": "നമസ്കാരം", "Thank you": "നന്ദി",
        "Help": "സഹായം", "Where is": "എവിടെ ആണ്",
        "Water": "വെള്ളം", "Food": "ഭക്ഷണം",
        "Yes": "അതെ", "No": "ഇല്ല",
        "Sorry": "ക്ഷമിക്കണം", "Good morning": "സുപ്രഭാതം",
    },
    "kn": {
        "Hello": "ನಮಸ್ಕಾರ", "Thank you": "ಧನ್ಯವಾದಗಳು",
        "Help": "ಸಹಾಯ", "Where is": "ಎಲ್ಲಿದೆ",
        "Water": "ನೀರು", "Food": "ಆಹಾರ",
        "Yes": "ಹೌದು", "No": "ಇಲ್ಲ",
        "Sorry": "ಕ್ಷಮಿಸಿ", "Good morning": "ಶುಭೋದಯ",
    },
}


@language_bp.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    text = (data.get("text") or "").strip()
    source = data.get("source_lang", "en")
    target = data.get("target_lang", "ta")

    if not text:
        return jsonify({"error": "text is required"}), 400

    if source == target:
        return jsonify({"original": text, "translated": text, "target_lang": target})

    # Check built-in dictionary first (accurate)
    builtin = BUILTIN_TRANSLATIONS.get((text.lower(), target))
    if builtin:
        return jsonify({"original": text, "translated": builtin, "target_lang": target, "source": "builtin"})

    # Fallback to MyMemory API
    try:
        resp = requests.get(TRANSLATE_URL,
                            params={"q": text, "langpair": f"{source}|{target}"},
                            timeout=10)
        result = resp.json()
        translated = result.get("responseData", {}).get("translatedText", "")
        if not translated or result.get("responseStatus") != 200:
            return jsonify({"error": "Translation failed. Try again."}), 502
        return jsonify({"original": text, "translated": translated, "target_lang": target, "source": "api"})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Translation service unavailable: {str(e)}"}), 503


@language_bp.route("/languages", methods=["GET"])
def supported_languages():
    return jsonify(SUPPORTED_LANGUAGES)


@language_bp.route("/phrases/<lang_code>", methods=["GET"])
def common_phrases(lang_code):
    phrases = COMMON_PHRASES.get(lang_code)
    if not phrases:
        return jsonify({"error": f"Phrases not available for '{lang_code}'"}), 404
    return jsonify({"language": SUPPORTED_LANGUAGES.get(lang_code, lang_code), "phrases": phrases})

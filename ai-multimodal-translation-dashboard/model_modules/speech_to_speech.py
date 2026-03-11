# model_modules/speech_to_speech.py

from transformers import AutoModelForSeq2SeqLM, NllbTokenizer
from faster_whisper import WhisperModel
from gtts import gTTS
import json
import os
import uuid

# Load language codes
with open("lang_codes.json", "r", encoding="utf-8") as f:
    LANG_CODES = json.load(f)

tts_voice_map = {
    "eng_Latn": "en",
    "hin_Deva": "hi",
    "mar_Deva": "mr",
    "guj_Gujr": "gu",
    "kan_Knda": "kn",
    "mal_Mlym": "ml",
    "tam_Taml": "ta",
    "tel_Telu": "te",
    "ben_Beng": "bn",
    "fra_Latn": "fr",
    "spa_Latn": "es"
}

iso_lang_map = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh",
    "Arabic": "ar",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Urdu": "ur",
    "Russian": "ru",
    "Japanese": "ja"
}

# Load models
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = NllbTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
whisper_model = WhisperModel("small", compute_type="int8", device="cpu")


def speech_to_speech_translate(audio_path, src_lang_name, tgt_lang_name):
    src_lang = LANG_CODES.get(src_lang_name)
    tgt_lang = LANG_CODES.get(tgt_lang_name)
    whisper_lang = iso_lang_map.get(src_lang_name)

    if not src_lang or not tgt_lang or not whisper_lang:
        return "Unsupported language", None, None

    try:
        # Step 1: Transcribe using Whisper
        segments, _ = whisper_model.transcribe(audio_path, language=whisper_lang)
        full_text = " ".join([seg.text.strip() for seg in segments])

        # Step 2: Translate with NLLB
        tokenizer.src_lang = src_lang
        inputs = tokenizer(full_text, return_tensors="pt", padding=True, truncation=True)
        generated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang))
        translated = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

        # Step 3: TTS output
        tts_lang = tts_voice_map.get(tgt_lang, "en")
        tts = gTTS(translated, lang=tts_lang)
        filename = f"tts_output_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join("static", filename)
        tts.save(filepath)

        return full_text, translated, f"/static/{filename}"

    except Exception as e:
        return f"Error: {str(e)}", None, None

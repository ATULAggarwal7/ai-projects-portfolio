# model_modules/text_to_speech.py

from transformers import AutoModelForSeq2SeqLM, NllbTokenizer
from gtts import gTTS
import json
import os
import uuid

# Load language codes
with open("lang_codes.json", "r", encoding="utf-8") as f:
    LANG_CODES = json.load(f)

model_name = "facebook/nllb-200-distilled-600M"
tokenizer = NllbTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Language code to voice mapping
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

def translate_and_speak(text, src_lang_name, tgt_lang_name):
    src_lang = LANG_CODES.get(src_lang_name)
    tgt_lang = LANG_CODES.get(tgt_lang_name)

    if not src_lang or not tgt_lang:
        return "Invalid language.", None

    tokenizer.src_lang = src_lang
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang))
    translated = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Generate TTS audio using gTTS
    tts_lang = tts_voice_map.get(tgt_lang, "en")  # default fallback to English
    tts = gTTS(translated, lang=tts_lang)
    filename = f"tts_output_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join("static", filename)
    tts.save(filepath)

    return translated, filename

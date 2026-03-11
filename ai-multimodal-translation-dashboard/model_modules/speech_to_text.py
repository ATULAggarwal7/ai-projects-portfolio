from faster_whisper import WhisperModel
from transformers import AutoModelForSeq2SeqLM, NllbTokenizer
import json

# Load language codes
with open("lang_codes.json", "r", encoding="utf-8") as f:
    LANG_CODES = json.load(f)

# Load NLLB model
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = NllbTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Load Whisper model
whisper_model = WhisperModel("small", compute_type="int8", device="cpu")

# ISO codes for Whisper
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

def translate_speech_text(audio_path, src_lang_name, tgt_lang_name):
    src_lang_code = LANG_CODES.get(src_lang_name)
    tgt_lang_code = LANG_CODES.get(tgt_lang_name)

    if not src_lang_code or not tgt_lang_code:
        return "Unsupported language.", ""

    whisper_lang_code = iso_lang_map.get(src_lang_name)
    if not whisper_lang_code:
        return "Whisper unsupported language.", ""

    # Transcribe with Whisper
    segments, info = whisper_model.transcribe(audio_path, language=whisper_lang_code)
    full_text = " ".join([seg.text.strip() for seg in segments])

    # Translate with NLLB
    tokenizer.src_lang = src_lang_code
    inputs = tokenizer(full_text, return_tensors="pt", padding=True, truncation=True)
    generated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang_code))
    translated = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    return full_text, translated  # ✅ Return both transcription and translation

from transformers import NllbTokenizer, AutoModelForSeq2SeqLM
import json

# Load lang code mapping
with open("lang_codes.json", "r", encoding="utf-8") as f:
    LANG_CODES = json.load(f)

model_name = "facebook/nllb-200-distilled-600M"
tokenizer = NllbTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def translate_text(text, src_lang_name, tgt_lang_name):
    if not text:
        return "No input text provided."

    src_lang = LANG_CODES.get(src_lang_name)
    tgt_lang = LANG_CODES.get(tgt_lang_name)

    if not src_lang or not tgt_lang:
        return "Unsupported language selected."

    tokenizer.src_lang = src_lang
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Set forced target language using BOS token ID
    inputs["forced_bos_token_id"] = tokenizer.convert_tokens_to_ids(tgt_lang)

    translated = model.generate(**inputs, max_length=512)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

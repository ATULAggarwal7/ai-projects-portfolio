# tts_engine.py
import os
import json
from TTS.api import TTS
from pydub import AudioSegment
from utils import apply_dictionary, split_text_into_chunks

# Config defaults
DICT_FILE = "dictionary.json"
SPEAKER_WAV = "audio_2.wav"
DEFAULT_OUTPUT_DIR = "samples"
MAX_CHARS = 250
CHUNK_SILENCE_MS = 100

# Load or init dictionary
if os.path.exists(DICT_FILE):
    with open(DICT_FILE, "r", encoding="utf-8") as f:
        custom_dict = json.load(f)
else:
    custom_dict = {}


def save_dictionary():
    with open(DICT_FILE, "w", encoding="utf-8") as f:
        json.dump(custom_dict, f, indent=4, ensure_ascii=False)


# Initialize TTS model lazily (so GUI can start quickly)
_tts = None


def get_tts(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False):
    global _tts
    if _tts is None:
        _tts = TTS(model_name, gpu=gpu)
    return _tts


def apply_user_dictionary(text):
    return apply_dictionary(text, custom_dict)


def combine_audio_chunks(
    text,
    output_file,
    model_name=None,
    speaker_wav=SPEAKER_WAV,
    language="en",
    speed=1.0,
    pitch=1.0,
    volume=0.0,
):
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    tts = get_tts(model_name) if model_name else get_tts()
    chunks = split_text_into_chunks(text, max_len=MAX_CHARS)

    combined = AudioSegment.silent(duration=0)
    for i, chunk in enumerate(chunks, 1):
        tmp = f"{output_file}.part{i}.wav"
        tts.tts_to_file(
            text=chunk,
            speaker_wav=speaker_wav,
            language=language,
            file_path=tmp,
        )
        audio = AudioSegment.from_wav(tmp)
        os.remove(tmp)

        # apply simple adjustments (speed/pitch via frame rate) if needed
        if speed != 1.0:
            new_frame_rate = int(audio.frame_rate * speed)
            audio = audio._spawn(
                audio.raw_data, overrides={"frame_rate": new_frame_rate}
            ).set_frame_rate(44100)

        if pitch != 1.0:
            new_sample_rate = int(audio.frame_rate * pitch)
            audio = audio._spawn(
                audio.raw_data, overrides={"frame_rate": new_sample_rate}
            ).set_frame_rate(44100)

        if volume != 0.0:
            audio += volume

        combined += audio + AudioSegment.silent(duration=CHUNK_SILENCE_MS)

    combined.export(output_file, format="wav")
    return output_file


def update_dictionary_entry(wrong_word, correction):
    key = wrong_word.lower().strip()
    if not key:
        return
    custom_dict[key] = correction
    save_dictionary()

from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import webbrowser
import socket
import json
import os

from model_modules.text_to_text import translate_text
from model_modules.text_to_speech import translate_and_speak
from model_modules.speech_to_text import translate_speech_text
from model_modules.speech_to_speech import speech_to_speech_translate


app = Flask(__name__)

# Load language list
with open("lang_codes.json", "r", encoding="utf-8") as f:
    LANGUAGES = list(json.load(f).keys())

def get_ip():
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1:5000"

@app.route("/")
def index():
    return render_template("index.html", languages=LANGUAGES)

# ✅ Text to Text
@app.route("/translate", methods=["POST"])
def handle_text_to_text():
    data = request.get_json()
    text = data.get("text")
    src = data.get("source_lang")
    tgt = data.get("target_lang")

    translated = translate_text(text, src, tgt)
    return jsonify({"translated_text": translated})

# ✅ Text to Speech
@app.route("/tts", methods=["POST"])
def handle_text_to_speech():
    data = request.get_json()
    text = data.get("text")
    src = data.get("source_lang")
    tgt = data.get("target_lang")

    translated, filename = translate_and_speak(text, src, tgt)
    if not filename:
        return jsonify({"error": "TTS failed"}), 500

    return jsonify({
        "translated_text": translated,
        "audio_file": f"/static/{filename}"
    })

# ✅ Speech to Text
@app.route("/speech_translate", methods=["POST"])
def handle_speech_to_text():
    if "audio" not in request.files:
        return jsonify({"error": "Audio file missing."}), 400

    file = request.files["audio"]
    src = request.form.get("source_lang")
    tgt = request.form.get("target_lang")

    filepath = f"temp_audio/{file.filename}"
    os.makedirs("temp_audio", exist_ok=True)
    file.save(filepath)

    transcribed_text, translated = translate_speech_text(filepath, src, tgt)

    return jsonify({
        "transcribed_text": transcribed_text,
        "translated_text": translated
    })

# ✅ Speech to Speech
@app.route("/speech_to_speech", methods=["POST"])
def handle_speech_to_speech():
    if "audio" not in request.files:
        return jsonify({"error": "Audio file missing."}), 400

    file = request.files["audio"]
    src = request.form.get("source_lang")
    tgt = request.form.get("target_lang")

    filepath = f"temp_audio/{file.filename}"
    os.makedirs("temp_audio", exist_ok=True)
    file.save(filepath)

    transcribed_text, translated_text, audio_file = speech_to_speech_translate(filepath, src, tgt)

    return jsonify({
        "transcribed_text": transcribed_text,
        "translated_text": translated_text,
        "audio_file": audio_file
    })

def open_browser():
    ip = get_ip()
    webbrowser.open(f"https://{ip}")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(host="0.0.0.0", port=5000, ssl_context=("certs/cert.pem", "certs/key.pem"))

# AI Multimodal Translation Dashboard

An AI-powered translation system that supports **speech-to-speech, speech-to-text, text-to-speech, and text-to-text translation** through an interactive web dashboard.

The project integrates multiple AI models into a single interface, enabling users to translate speech and text across multiple languages in real time.

---

## Features

* Speech-to-Speech Translation
* Speech-to-Text Transcription
* Text-to-Speech Generation
* Text-to-Text Translation
* Interactive Web Dashboard
* Multi-language support

---

## Project Structure

```
ai-multimodal-translation-dashboard
│
├── server.py
├── lang_codes.json
│
├── model_modules
│   ├── speech_to_speech.py
│   ├── speech_to_text.py
│   ├── text_to_speech.py
│   └── text_to_text.py
│
├── templates
│   └── index.html
│
├── static
│   └── style.css
│
├── certs
│   ├── cert.pem
│   └── key.pem
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```
git clone https://github.com/ATULAggarwal7/ai-projects-portfolio
```

Navigate to the project folder:

```
cd ai-multimodal-translation-dashboard
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Running the Project

Start the server:

```
python server.py
```

Open your browser and go to:

```
http://localhost:8000
```

The translation dashboard will appear.

---

## Supported Translation Modes

1. Speech to Speech
2. Speech to Text
3. Text to Speech
4. Text to Text

Users can select input language, output language, and translation mode directly from the dashboard.

---

## Technologies Used

* Python
* FastAPI / Flask backend
* Speech Recognition
* Text-to-Speech models
* Neural Machine Translation
* HTML / CSS dashboard

---

## Applications

* Real-time language translation
* Speech transcription
* Voice assistants
* Multilingual communication tools
* AI powered translation interfaces

---

## Author

Atul Aggarwal
AI / Machine Learning Projects Portfolio

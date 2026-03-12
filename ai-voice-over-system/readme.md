# AI Voice Over Generation System

## Overview

This project is an **AI-powered voice generation system** that converts text into natural speech using a multilingual Text-to-Speech model.

The application provides a **desktop GUI interface** that allows users to generate speech from **CSV files or manual text input**. It also supports **custom pronunciation dictionaries, adjustable speech parameters, and voice cloning using reference audio**.

This project demonstrates the integration of **AI speech synthesis, GUI applications, and audio processing**.

---

## Key Features

* Text to Speech using **XTTS v2 AI model**
* **CSV batch voice generation**
* Manual text → speech conversion
* Adjustable **speed, pitch, and volume**
* Custom pronunciation dictionary
* Automatic audio chunking for long text
* Audio merging into a single output file
* Simple desktop GUI built with **Tkinter**

---

## System Architecture

```
Text / CSV Input
       ↓
Custom Dictionary Processing
       ↓
Text Chunking
       ↓
XTTS v2 TTS Model
       ↓
Audio Processing (Speed / Pitch / Volume)
       ↓
Final Speech Output
```

---

## Project Structure

```
ai-voice-over-system
│
├── main.py                # GUI application
├── tts_engine.py          # TTS generation engine
├── utils.py               # text processing utilities
├── requirements.txt       # project dependencies
│
├── sentences.csv          # example CSV input
├── dictionary.json        # custom pronunciation dictionary
├── audio_2.wav            # reference voice sample
│
├── samples
│   └── manual_text.wav    # generated audio output
```

---

## Important Components

### main.py

Main GUI application built using **Tkinter**.

Features:

* CSV loading
* Manual text input
* Speech parameter control
* Audio generation control

---

### tts_engine.py

Core **text-to-speech engine**.

Responsible for:

* loading XTTS model
* generating speech
* splitting long text into chunks
* combining generated audio
* applying speed/pitch/volume modifications

---

### utils.py

Utility functions for:

* text preprocessing
* pronunciation correction
* chunking long text

---

### dictionary.json

Stores custom pronunciation corrections.

Example:

```
{
  "AI": "A I",
  "NVIDIA": "en-vid-ee-ah"
}
```

---

### sentences.csv

Example CSV file used for **batch voice generation**.

---

## Installation

Clone the repository

```
git clone https://github.com/ATULAggarwal7/ai-projects-portfolio
```

Navigate to the project folder

```
cd ai-voice-over-system
```

Install dependencies

```
pip install -r requirements.txt
```

---

## Running the Application

Run the GUI application:

```
python main.py
```

The interface allows you to:

* Load CSV files
* Enter manual text
* Adjust speech parameters
* Generate voice output

---

## Technologies Used

* Python
* Coqui TTS (XTTS v2)
* Tkinter GUI
* Pandas
* Pydub
* Audio processing

---

## Applications

* Voice over generation
* Automated narration systems
* Content creation
* Speech accessibility tools
* AI voice assistants

---

## Author

Atul Aggarwal

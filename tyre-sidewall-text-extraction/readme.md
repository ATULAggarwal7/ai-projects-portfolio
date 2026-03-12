# Tyre Text Extraction using Super Resolution and OCR

## Overview

This project extracts **text from tyre sidewall images** using a combination of **image enhancement and OCR**.

Tyre images often contain curved text and low contrast which makes recognition difficult.
To improve recognition accuracy, this system first enhances the image using **Real-ESRGAN super resolution** and then applies **EasyOCR** to extract the text.

---

## System Pipeline

Tyre Image → Super Resolution Enhancement → OCR → Extracted Text

1. Input tyre image is loaded.
2. Image quality is enhanced using **Real-ESRGAN**.
3. The enhanced image is passed to **EasyOCR**.
4. The detected text from the tyre sidewall is printed as output.

---

## Features

* Image enhancement using **Real-ESRGAN**
* OCR using **EasyOCR**
* Works on low-quality tyre images
* Simple computer vision pipeline
* Sample tyre images included

---

## Project Structure

```
tyre-text-extraction-with-super-resolution
│
├── main.py
├── super_resolution.py
├── requirements.txt
│
├── sample_images
│   ├── img.jpeg
│   ├── img1.jpeg
│   └── ...
│
├── weights
│   └── RealESRGAN_x2plus.pth
│
└── README.md
```

---

## Installation

Clone the repository

```
git clone https://github.com/ATULAggarwal7/ai-projects-portfolio
```

Install dependencies

```
pip install -r requirements.txt
```

---

## Run the Project

```
python main.py
```

The system will:

1. Enhance the tyre image
2. Detect text
3. Print extracted tyre markings

---

## Technologies Used

* Python
* OpenCV
* EasyOCR
* Real-ESRGAN
* NumPy

---

## Applications

* Tyre manufacturing inspection
* Vehicle service automation
* Automotive inventory systems
* Computer vision research

---

## Author

Atul Aggarwal

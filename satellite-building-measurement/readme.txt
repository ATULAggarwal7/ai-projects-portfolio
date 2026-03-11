# Satellite Building Size & Height Estimator

A computer vision tool that estimates **building size and approximate height from satellite images** using pixel-to-meter calibration.

The system allows users to measure **real-world distances and areas** directly from satellite imagery by converting pixel measurements into **actual physical units**.

---

## 📌 Features

* Pixel-to-meter calibration from satellite images
* Building footprint measurement
* Approximate building height estimation
* Interactive measurement using mouse clicks
* Works with any high-resolution aerial or satellite imagery

---

## 🧠 How It Works

Satellite images are composed of pixels, but real-world measurements require conversion to **meters or feet**.

This project uses a **calibration step** to calculate the scale of the image.

### Workflow

```
Satellite Image
      ↓
User selects reference points
      ↓
Pixel-to-meter calibration
      ↓
User outlines building area
      ↓
Area calculation
      ↓
Approximate building height estimation
```

---

## 📂 Project Structure

```
satellite-building-measurement
│
├── scale_calibrator.py            # Calculates pixel-to-meter scale
├── building_measurement.py        # Estimates building size and height
├── pixels_per_meter.txt           # Stores calibration value
│
├── data
│   └── sample_image.jpg           # Example satellite image
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Install required dependencies:

```
pip install opencv-python numpy matplotlib pillow
```

Or install using the requirements file:

```
pip install -r requirements.txt
```

---

## ▶️ How to Use

### Step 1 — Calibrate the Image

Run the calibration script:

```
python scale_calibrator.py
```

Select **two points on the image with a known real-world distance**.

Example:

```
Real distance = 50 meters
```

The system will calculate:

```
pixels_per_meter
```

and store it in:

```
pixels_per_meter.txt
```

---

### Step 2 — Measure Building Dimensions

Run the measurement tool:

```
python building_measurement.py
```

Steps:

1. Select the building region
2. The system calculates the **building footprint area**
3. Estimate the **approximate building height**

---

## 📊 Output

The program displays:

* Building footprint area
* Estimated building dimensions
* Approximate building height

Example output:

```
Building Area : 850 m²
Estimated Height : 120 ft
```

---

## 🚀 Applications

This tool can be used in:

* Urban planning
* Architecture and infrastructure analysis
* Remote sensing studies
* GIS research
* Land-use monitoring

---

## 🛠 Technologies Used

* Python
* OpenCV
* NumPy
* Matplotlib

---

## 📌 Limitations

* Height estimation is **approximate**
* Satellite images provide **top-down views**, so height estimation depends on assumptions such as floor height.

---

## 📌 Future Improvements

Possible improvements include:

* Automatic building detection using deep learning
* Shadow-based height estimation
* Integration with GIS tools
* Web-based satellite measurement interface

---

## 👨‍💻 Author

**Atul Aggarwal**

AI / Machine Learning Projects Portfolio

# AI Building Footprint Estimator

An AI-powered tool that detects buildings in satellite imagery and estimates **building footprint area and approximate height** using the **Segment Anything Model (SAM)**.

The system combines **computer vision, deep learning, and geospatial measurement techniques** to analyze satellite images and extract structural information.

---

## 🚀 Features

* Automatic **building segmentation using AI**
* Interactive **pixel-to-meter calibration**
* Building **footprint area estimation**
* Approximate **building height estimation**
* Works with high-resolution satellite or aerial imagery
* Visual output with segmentation overlays

---

## 🧠 Model Used

This project uses the **Segment Anything Model (SAM)** developed by Meta AI for automatic segmentation.

SAM is a powerful vision model capable of detecting objects from minimal prompts such as clicks.

Model used in this project:

```
sam_vit_h
```

---

## 📂 Project Structure

```
ai-building-footprint-estimator
│
├── app.py                      # Main program
│
├── src
│   ├── calibration.py          # Pixel-to-meter calibration
│   ├── sam_wrapper.py          # SAM segmentation wrapper
│   ├── height_from_mask.py     # Building height estimation
│   └── utils.py                # Utility functions
│
├── data
│   └── sample_image.jpg        # Example satellite image
│
├── models
│   └── sam_vit_h.pth           # SAM model (download separately)
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository or download the project.

Install dependencies:

```
pip install -r requirements.txt
```

---

## 📥 Download the Model

The SAM model is too large to store in this repository.

Download it from the official source:

```
https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
```

After downloading, rename the file to:

```
sam_vit_h.pth
```

Then place it in the **models/** folder.

Expected structure:

```
ai-building-footprint-estimator
│
├── models
│   └── sam_vit_h.pth
```

---

## ▶️ How to Run the Project

Run the main script:

```
python app.py
```

---

## 🧭 Workflow

1. The program loads the satellite image.
2. User performs **image calibration** by selecting two points with a known distance.
3. The system calculates **pixel-to-meter scale**.
4. User clicks on a building in the image.
5. The **SAM model automatically segments the building**.
6. The system calculates:

   * Building footprint area
   * Approximate building height
7. Results are saved in the **output folder**.

---

## 📊 Output

The program generates:

* Segmented building mask
* Annotated image
* Building measurement information

Example results:

```
Building Area : 850 m²
Estimated Height : 30 m
```

---

## 🛠 Technologies Used

* Python
* PyTorch
* Segment Anything Model (SAM)
* OpenCV
* NumPy
* Matplotlib

---

## 📌 Applications

This system can be used for:

* Urban planning
* Infrastructure analysis
* Satellite image analysis
* GIS research
* Remote sensing applications

---

## 📌 Future Improvements

Possible improvements include:

* Automatic detection of multiple buildings
* Integration with GIS tools
* Shadow-based height estimation
* Web interface for satellite analysis

---

## 👨‍💻 Author

Atul Aggarwal

AI / Machine Learning Projects Portfolio

# Satellite Image Segmentation using Deep Learning

A computer vision project that performs **semantic segmentation on satellite imagery** using a deep learning model.
The system classifies each pixel of a satellite image into different land-cover categories such as **buildings, roads, vegetation, and water**.

This project demonstrates how **PyTorch-based deep learning models** can be used for **geospatial analysis and satellite scene understanding**.

---

## 📌 Features

* Deep learning based **semantic segmentation**
* Detects different land-cover types from satellite images
* Generates **pixel-wise classification masks**
* Produces **colored segmentation overlays**
* Simple inference pipeline for running predictions on new images

---

## 🧠 Model Used

The project uses a **Fully Convolutional Network (FCN) with a ResNet50 backbone** for semantic segmentation.

Model capabilities:

* Pixel-wise classification
* Multi-class segmentation
* Works on aerial and satellite imagery

---

## 📂 Project Structure

```
satellite-image-segmentation
│
├── model
│   └── segmentation_model.pth      # Trained segmentation model
│
├── data
│   └── sample_image.jpg            # Example satellite image
│
├── inference.py                    # Runs segmentation inference
├── requirements.txt                # Required Python packages
└── README.md
```

---

## ⚙️ Installation

Clone the repository or download the project.

Install dependencies:

```
pip install -r requirements.txt
```

Or install manually:

```
pip install torch torchvision opencv-python matplotlib pillow numpy
```

---

## ▶️ How to Run

Place a satellite image inside the **data** folder.

Run the inference script:

```
python inference.py
```

The model will process the image and generate segmentation outputs.

---

## 📊 Output

The system generates:

* **Raw segmentation mask**
* **Colored segmentation mask**
* **Overlay image with segmentation results**

Example output:

```
segmented_overlay.png
colored_mask.png
raw_mask.png
```

---

## 🚀 Applications

Satellite image segmentation can be used for:

* Urban planning
* Land-use analysis
* Environmental monitoring
* Disaster assessment
* Geospatial AI applications

---

## 🛠 Technologies Used

* Python
* PyTorch
* Torchvision
* OpenCV
* NumPy
* Matplotlib

---

## 📌 Future Improvements

Possible enhancements for this project:

* Add more segmentation classes
* Use advanced models such as **DeepLabV3 or SegFormer**
* Train on larger satellite datasets
* Deploy as a **web application for real-time satellite analysis**

---

## 👨‍💻 Author

**Atul Aggarwal**

AI / Machine Learning Projects Portfolio

# IoT Temperature Monitoring System with QR Dashboard

## Overview

This project is an **IoT-based environmental monitoring system** that collects **temperature and humidity data using a DHT11 sensor connected to Arduino** and sends the data to a **Python server** for logging, prediction, and visualization.

The system provides a **web dashboard** that displays sensor readings and can be accessed through a **QR code** for quick monitoring.

This project demonstrates the integration of **IoT hardware, backend development, and machine learning prediction**.

---

## System Architecture

Sensor (DHT11) → Arduino → Python Server → Data Storage → Web Dashboard → QR Access

1. The **DHT11 sensor** measures temperature and humidity.
2. **Arduino** reads the sensor data.
3. Data is sent to the **Python backend server**.
4. The server logs the data in **CSV format**.
5. A **machine learning model** analyzes the data.
6. A **web dashboard** displays the readings.
7. Users can access the dashboard using a **QR code**.

---

## Hardware Used

* Arduino Board
* DHT11 Temperature and Humidity Sensor
* Jumper Wires
* USB Cable
* Computer for server

---

## Hardware Setup

The following image shows the **Arduino and DHT11 sensor connection setup**.

![Arduino DHT11 Setup](Arduino_Code/setup.jpg)

*(Make sure the image filename matches your uploaded picture name.)*

---

## Project Structure

```
iot-temperature-monitoring-system
│
├── Arduino_Code
│   ├── Arduino_Code.ino
│   └── setup.jpg
│
├── templates
│   └── dashboard.html
│
├── data
│   └── sample_data.csv
│
├── qr_codes
│   └── example_qr.png
│
├── server.py
├── DHT11_model.pkl
├── requirements.txt
└── README.md
```

---

## Key Components

### Arduino Code

Reads temperature and humidity from the **DHT11 sensor** and sends the data to the server.

### Python Server (`server.py`)

Responsible for:

* Receiving sensor data
* Saving readings to CSV
* Running machine learning predictions
* Serving the web dashboard

### Dashboard

The **HTML dashboard** displays sensor readings and prediction results.

### Machine Learning Model

A trained model (`DHT11_model.pkl`) predicts environmental patterns based on sensor data.

### QR Code Access

A generated **QR code** allows users to quickly open the monitoring dashboard on their device.
Optional: To expose the dashboard to the internet, install Cloudflare Tunnel (cloudflared).
---

## Installation

Clone the repository:

```
git clone https://github.com/yourusername/ai-projects-portfolio.git
```

Navigate to the project folder:

```
cd iot-temperature-monitoring-system
```

Install required dependencies:

```
pip install -r requirements.txt
```

---

## Running the System

### Step 1 — Upload Arduino Code

Upload `Arduino_Code.ino` to your Arduino board using the Arduino IDE.

### Step 2 — Start the Python Server

Run:

```
python server.py
```

### Step 3 — Access Dashboard

Open the browser and visit:

```
http://localhost:5000
```

You can also scan the **QR code** to access the dashboard.

---

## Technologies Used

* Python
* Flask
* Pandas
* Scikit-learn
* Arduino
* HTML Dashboard
* IoT Sensors

---

## Features

* Real-time temperature monitoring
* Humidity tracking
* Machine learning prediction
* Web dashboard visualization
* QR code based dashboard access
* Data logging in CSV format

---

## Applications

* Smart home monitoring
* Industrial environment monitoring
* Server room temperature monitoring
* IoT research and experimentation

---

## Author

Atul Aggarwal

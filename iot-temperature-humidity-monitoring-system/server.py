from flask import Flask, jsonify, render_template
import serial
import serial.tools.list_ports
import joblib
import threading
import time
import pandas as pd
from datetime import datetime
import subprocess
import re
import webbrowser
import os
import qrcode

app = Flask(__name__)
model = joblib.load("DHT11_model.pkl")

latest_temp = None
latest_hum = None
latest_status = None
latest_time = None

room_id = "room1"
public_url = None


# Auto-detect Arduino
def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "Arduino" in port.description or "USB Serial" in port.description:
            return port.device
    return None


arduino_port = find_arduino_port()
if arduino_port:
    try:
        ser = serial.Serial(arduino_port, 9600, timeout=1)
        time.sleep(2)
        print(f"Arduino connected on {arduino_port}")
    except Exception as e:
        print(f"Error opening port {arduino_port}: {e}")
        ser = None
else:
    print("Arduino not found.")
    ser = None


# Background thread to read sensor
def read_from_arduino():
    global latest_temp, latest_hum, latest_status, latest_time
    if not ser:
        print("No serial connection.")
        return

    os.makedirs("data", exist_ok=True)
    csv_file = f"data/{room_id}_data.csv"

    # Write header only if file doesn't exist
    if not os.path.exists(csv_file):
        with open(csv_file, "w") as f:
            f.write("Time,Temperature (°C),Humidity (%),Status\n")

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(',')
                if len(parts) == 2:
                    temp = float(parts[0])
                    hum = float(parts[1])
                    input_df = pd.DataFrame([[temp, hum]], columns=["Temperature (°C)", "Humidity (%)"])
                    prediction = model.predict(input_df)[0]
                    status = "NORMAL" if prediction == 0 else "FAILURE"

                    latest_temp = temp
                    latest_hum = hum
                    latest_status = status
                    latest_time = datetime.now().strftime("%H:%M:%S")

                    print(f"Temp: {temp}C | Humidity: {hum}% | Status: {status}")

                    # Append to CSV
                    with open(csv_file, "a") as f:
                        f.write(f"{latest_time},{temp},{hum},{status}\n")

            time.sleep(1)
        except Exception as e:
            print("Error reading Arduino:", e)



# Status endpoint
@app.route('/get_status', methods=['GET'])
def get_status():
    if latest_temp is None or latest_hum is None or latest_status is None:
        return jsonify({'error': 'No data yet from sensor'}), 503
    return jsonify({
        'temperature': latest_temp,
        'humidity': latest_hum,
        'status': latest_status,
        'timestamp': latest_time
    })

@app.route('/status/<room>')
def status_page(room):
    return render_template('dashboard.html', room=room)


@app.route('/status_only/<room>')
def status_only(room):
    color = "green" if latest_status == "NORMAL" else "red"
    return f"""
    <html>
        <head><title>Status</title></head>
        <body style="display: flex; justify-content: center; align-items: center; height: 100vh; background-color: black;">
            <div style="color: {color}; font-size: 48px; font-weight: bold;">{latest_status}</div>
        </body>
    </html>
    """




@app.route('/')
def dashboard():
    return render_template('dashboard.html')


# QR generator
def generate_qr_code(link):
    os.makedirs("qr_codes", exist_ok=True)
    qr_img = qrcode.make(link)
    qr_path = f"qr_codes/{room_id}_qr.png"
    qr_img.save(qr_path)
    print(f"\n[QR] QR Code saved at: {qr_path}")
    print(f"[QR] Scan this URL: {link}\n")


# Cloudflare tunnel and public URL extraction
def start_cloudflare_tunnel():
    global public_url
    try:
        print("Starting Cloudflare Tunnel...")
        tunnel = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", "http://localhost:5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        for line in tunnel.stdout:
            print(line.strip())
            match = re.search(r"https://[-a-zA-Z0-9]+\.trycloudflare\.com", line)
            if match:
                public_url = match.group(0)
                status_url = f"{public_url}/status_only/{room_id}"  # <-- NEW endpoint 
                print(f"\nPublic URL: {public_url}\n")
                generate_qr_code(status_url)
                break
    except Exception as e:
        print("Cloudflare Tunnel error:", e)


# Auto-open browser to dashboard
def open_browser():
    time.sleep(3)
    webbrowser.open("http://127.0.0.1:5000")


# Background thread for sensor
if ser:
    threading.Thread(target=read_from_arduino, daemon=True).start()

# Start everything
if __name__ == '__main__':
    print("Starting Server and Tunnel...\n")
    threading.Thread(target=start_cloudflare_tunnel, daemon=True).start()
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)

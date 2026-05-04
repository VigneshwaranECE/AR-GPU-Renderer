import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime

# ML
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

# 🔥 LOAD MODEL
model = joblib.load("gpu_model.pkl")

latest_data = {
    "gpu_temp": 0,
    "time": "",
    "unit": "°C"
}

last_update_time = None


# ===============================
# 🔥 RECEIVE DATA FROM SENDER
# ===============================
@app.route('/api/update-gpu', methods=['POST'])
def update_gpu():
    global latest_data, last_update_time

    data = request.get_json()

    print("🔥 RECEIVED DATA:", data)  # DEBUG

    latest_data = {
        "gpu_temp": data.get("gpu_temp", 0),
        "time": data.get("time", ""),
        "unit": "°C"
    }

    last_update_time = datetime.utcnow()

    return jsonify({"status": "updated"})


# ===============================
# 🔥 SEND DATA TO CLIENT (UNITY / BROWSER)
# ===============================
@app.route('/api/gpu-temp')
def gpu_temp():
    global last_update_time

    # ❌ NO DATA RECEIVED
    if last_update_time is None:
        return jsonify({
            "gpu_temp": 0,
            "time": "",
            "status": "OFF",
            "condition": "OFF"
        })

    # ❌ DATA TIMEOUT
    diff = (datetime.utcnow() - last_update_time).total_seconds()

    if diff > 6:
        return jsonify({
            "gpu_temp": 0,
            "time": "",
            "status": "OFF",
            "condition": "OFF"
        })

    # ✅ VALID DATA → ML PREDICTION
    temp = latest_data["gpu_temp"]

    input_data = pd.DataFrame([[temp]], columns=["temperature"])
    pred = model.predict(input_data)[0]

    if pred == 0:
        condition = "GOOD"
    elif pred == 1:
        condition = "WARNING"
    else:
        condition = "CRITICAL"

    return jsonify({
        **latest_data,
        "status": "ON",
        "condition": condition
    })


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

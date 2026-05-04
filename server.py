import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

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
# 🔥 SEND DATA (NO ML HERE)
# ===============================
@app.route('/api/gpu-temp')
def gpu_temp():
    global last_update_time

    # ❌ NO DATA RECEIVED
    if last_update_time is None:
        return jsonify({
            "gpu_temp": 0,
            "time": "",
            "status": "OFF"
        })

    # ❌ DATA TIMEOUT
    diff = (datetime.utcnow() - last_update_time).total_seconds()

    if diff > 6:
        return jsonify({
            "gpu_temp": 0,
            "time": "",
            "status": "OFF"
        })

    # ✅ ONLY RAW DATA (NO CONDITION)
    return jsonify({
        **latest_data,
        "status": "ON"
    })


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

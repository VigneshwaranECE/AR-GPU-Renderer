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


@app.route('/api/update-gpu', methods=['POST'])
def update_gpu():
    global latest_data, last_update_time

    data = request.json

    latest_data = {
        "gpu_temp": data.get("gpu_temp", 0),
        "time": data.get("time", ""),
        "unit": "°C"
    }

    last_update_time = datetime.utcnow()

    return jsonify({"status": "updated"})


@app.route('/api/gpu-temp')
def gpu_temp():
    global last_update_time

    # ❌ No data ever received
    if last_update_time is None:
        return jsonify({
            "gpu_temp": 0,
            "time": "",
            "status": "OFF"
        })

    # ❌ No recent update → PC OFF
    diff = (datetime.utcnow() - last_update_time).total_seconds()

    if diff > 6:  # 🔥 FAST detection
        return jsonify({
            "gpu_temp": 0,
            "time": "",
            "status": "OFF"
        })

    # ✅ PC ON
    return jsonify({
        **latest_data,
        "status": "ON"
    })


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

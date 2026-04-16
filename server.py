import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔥 store latest GPU data
latest_data = {
    "gpu_temp": 0,
    "time": "",
    "unit": "°C"
}

# ✅ RECEIVE DATA FROM YOUR PC
@app.route('/api/update-gpu', methods=['POST'])
def update_gpu():
    global latest_data

    data = request.json

    latest_data = {
        "gpu_temp": data.get("gpu_temp", 0),
        "time": data.get("time", ""),
        "unit": "°C"
    }

    return jsonify({"status": "updated"})


# ✅ SEND DATA TO UNITY
@app.route('/api/gpu-temp')
def gpu_temp():
    return jsonify(latest_data)


# UI page
@app.route('/')
def home():
    return render_template("index.html")


# RUN
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

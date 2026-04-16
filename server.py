import os
import subprocess
from datetime import datetime
from flask import Flask, jsonify, render_template   # ✅ added render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------- GPU FUNCTION ----------------

def get_gpu_temperature():
    try:
        result = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"]
        )
        temp = result.decode("utf-8").strip()
        return int(temp)

    except Exception as e:
        return str(e)


# ---------------- API ----------------

@app.route('/api/gpu-temp')
def gpu_temp():
    try:
        temp = get_gpu_temperature()

        # 🕒 Get current time
        current_time = datetime.now().strftime("%I:%M:%S %p")

        return jsonify({
            "gpu_temp": temp,
            "unit": "°C",
            "time": current_time
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ---------------- UI PAGE ----------------

@app.route('/')
def home():
    return render_template("index.html")   # ✅ now loads graph page


# ---------------- RUN ----------------

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
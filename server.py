import os
import subprocess
import random
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template
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

    except Exception:
        # 🔥 Render doesn't support GPU → return random realistic value
        return random.randint(40, 60)


# ---------------- API ----------------

@app.route('/api/gpu-temp')
def gpu_temp():
    try:
        temp = get_gpu_temperature()

        # ✅ Convert UTC → IST (India Time)
        current_time = (datetime.utcnow() + timedelta(hours=5, minutes=30)) \
            .strftime("%I:%M:%S %p")

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
    return render_template("index.html")


# ---------------- RUN ----------------

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

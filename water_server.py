from flask import Flask, jsonify
from flask_cors import CORS
import random
import threading
import time
import os

app = Flask(__name__)

# ENABLE CORS
CORS(app)

# ----------------------------------------
# GLOBAL WATER DATA
# ----------------------------------------

water_data = {
    "water_level": 35,
    "flood_risk": "Low",
    "ph_level": 7.1,
    "water_condition": "Safe",
    "day": "Day 1"
}

# ----------------------------------------
# DAY COUNTER
# ----------------------------------------

day_counter = 0

# ----------------------------------------
# UPDATE DATA EVERY 5 SECONDS
# ----------------------------------------

def update_water_data():

    global water_data
    global day_counter

    while True:

        # ----------------------------------------
        # RANDOM WATER LEVEL
        # ----------------------------------------

        water_level = random.randint(30, 100)

        # ----------------------------------------
        # FLOOD RISK LOGIC
        # ----------------------------------------

        if water_level <= 50:
            flood_risk = "Low"

        elif water_level <= 75:
            flood_risk = "Medium"

        else:
            flood_risk = "High"

        # ----------------------------------------
        # RANDOM pH LEVEL
        # ----------------------------------------

        ph_level = round(random.uniform(5.5, 8.8), 1)

        # ----------------------------------------
        # WATER CONDITION
        # ----------------------------------------

        if ph_level < 6.5:
            water_condition = "Acidic/Unsafe"

        elif ph_level > 8.5:
            water_condition = "Alkaline/Unsafe"

        else:
            water_condition = "Safe"

        # ----------------------------------------
        # DAY COUNTER
        # ----------------------------------------

        day_counter += 1

        day_label = f"Day {day_counter}"

        # ----------------------------------------
        # UPDATE JSON DATA
        # ----------------------------------------

        water_data = {
            "water_level": water_level,
            "flood_risk": flood_risk,
            "ph_level": ph_level,
            "water_condition": water_condition,
            "day": day_label
        }

        # ----------------------------------------
        # TERMINAL OUTPUT
        # ----------------------------------------

        print("\n--------------------------------")
        print("REAL-TIME WATER DATA UPDATED")
        print("--------------------------------")
        print(f"Day            : {day_label}")
        print(f"Water Level    : {water_level}%")
        print(f"Flood Risk     : {flood_risk}")
        print(f"pH Level       : {ph_level}")
        print(f"Water Condition: {water_condition}")

        # WAIT 5 SECONDS
        time.sleep(5)

# ----------------------------------------
# API ROUTE
# ----------------------------------------

@app.route('/waterdata', methods=['GET'])
def get_water_data():

    return jsonify(water_data)

# ----------------------------------------
# MAIN
# ----------------------------------------

if __name__ == '__main__':

    # START BACKGROUND THREAD
    threading.Thread(
        target=update_water_data,
        daemon=True
    ).start()

    # RENDER PORT
    port = int(os.environ.get("PORT", 5050))

    # RUN SERVER
    app.run(
        host='0.0.0.0',
        port=port,
        threaded=True
    )

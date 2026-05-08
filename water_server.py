from flask import Flask, jsonify
import random
import threading
import time
from datetime import datetime

app = Flask(__name__)

# ----------------------------------------
# GLOBAL WATER DATA
# ----------------------------------------

water_data = {
    "water_level": 35,
    "flood_risk": "Low",
    "ph_level": 7.1,
    "water_condition": "Safe",
    "last_updated": ""
}

# ----------------------------------------
# UPDATE DATA EVERY 5 SECONDS
# ----------------------------------------

def update_water_data():

    global water_data

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
        # Indian Safe Range = 6.5 - 8.5
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
        # REAL-TIME TIMESTAMP
        # ----------------------------------------

        current_time = datetime.now().strftime("%I:%M:%S %p")

        # ----------------------------------------
        # UPDATE JSON DATA
        # ----------------------------------------

        water_data = {
            "water_level": water_level,
            "flood_risk": flood_risk,
            "ph_level": ph_level,
            "water_condition": water_condition,
            "last_updated": current_time
        }

        # ----------------------------------------
        # TERMINAL OUTPUT
        # ----------------------------------------

        print("\n--------------------------------")
        print("REAL-TIME WATER DATA UPDATED")
        print("--------------------------------")
        print(f"Last Updated   : {current_time}")
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
    threading.Thread(target=update_water_data, daemon=True).start()

    # RUN FLASK SERVER
    app.run(host='0.0.0.0', port=5050)
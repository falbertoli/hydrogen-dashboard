from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow frontend requests
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # Allow Vue frontend

# Constants for calculations
TANK_WIDTH = 10.1667  # ft
TANK_LENGTH = 56.5  # ft
WATER_CAP = 18014 / 7.48052  # gal to ft³
TANK_ULLAGE = 0.05  # 5% volume loss due to ullage
EVAPORATION = 0.9925  # 99.25% LH2 retention per day
H2_DENS = 4.43  # lbs/ft³ (liquid hydrogen density)
SAFETY_DISTANCE = 1000  # Example: Min distance required from buildings

def compute_h2_demand(fleet_percentage, ground_vehicles, time_period):
    """Compute hydrogen demand and required storage"""
    fleet_percentage = int(fleet_percentage)  # 🔹 Ensure it's an integer
    time_multiplier = int(time_period.split()[0])  # Convert "7 days" → 7

    demand_factor = 10  # Example factor per fleet percentage
    vehicle_factor = 5  # Example H2 consumption per vehicle

    estimated_h2_demand = (fleet_percentage * demand_factor) + (len(ground_vehicles) * vehicle_factor)
    estimated_h2_demand *= time_multiplier

    storage_needed = estimated_h2_demand / H2_DENS  # Convert to ft³
    return estimated_h2_demand, storage_needed

def get_compliant_areas(required_storage_area):
    airport_areas = [
        {"name": "Zone 1", "space": 60000, "coordinates": [[33.6405, -84.4265], [33.6405, -84.4295], [33.6425, -84.4295], [33.6425, -84.4265]]},
        {"name": "Zone 2", "space": 30000, "coordinates": [[33.6410, -84.4280], [33.6410, -84.4310], [33.6430, -84.4310], [33.6430, -84.4280]]},
    ]

    compliant_zones = [area for area in airport_areas if area['space'] >= required_storage_area]
    return compliant_zones

def compute_max_storage(storage_area):
    """Compute max hydrogen storage for a given area"""
    tank_h2_storage = WATER_CAP * (1 - TANK_ULLAGE) * EVAPORATION  # Usable H₂ per tank
    tank_area = TANK_WIDTH * TANK_LENGTH  # Area occupied by one tank
    num_tanks = storage_area / tank_area  # Max tanks in available area

    total_h2_stored = num_tanks * tank_h2_storage  # Total hydrogen stored
    return total_h2_stored

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        print("Received data:", data)

        calc_mode = data.get("calculationMode", "demand")

        if calc_mode == "demand":
            fleet_percentage = data.get('fleetPercentage', 0)
            selected_vehicles = data.get('selectedVehicles', [])
            selected_time_period = data.get('selectedTimePeriod', "7 days")

            # Calculate hydrogen demand and storage needed
            h2_demand, storage_needed = compute_h2_demand(fleet_percentage, selected_vehicles, selected_time_period)

            # Find compliant areas based on storage and regulations
            compliant_zones = get_compliant_areas(storage_needed)

            response = {
                "estimatedH2Demand": h2_demand,
                "requiredStorageArea": storage_needed,
                "storageLocationFound": storage_needed,  # Example rule
                "compliantZones": compliant_zones
            }

        elif calc_mode == "storage":
            storage_area = int(data.get('storageArea', 0))
            max_h2_stored = storage_area / 5  # Example

            response = {
                "maxHydrogenStored": max_h2_stored
            }

        print("API Response:", response)
        return jsonify(response)

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
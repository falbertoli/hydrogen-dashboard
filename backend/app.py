# backend/app.py
"""
This Flask application provides API endpoints for hydrogen demand, economic impact, and storage cost calculations.
It interacts with SQLite databases to retrieve and process data.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from hydrogen_demand_tool import h2_demand_ac, h2_demand_gse
from economic_impact import hydrogen_uti_rev
from storage_cost import calculate_h2_storage_cost
import os

app = Flask(__name__) # create a Flask app instance
CORS(app, resources={r"/*": {"origins": "*"}}) # Enable CORS for all routes (r"/*) allowing requests from any origin ("*")

@app.route('/h2_demand_ac', methods=['POST']) # Dercorator maps the /h2_demand_ac URL to the h2_demand_ac_endpoint function.
def h2_demand_ac_endpoint():
    """
    API endpoint to calculate hydrogen demand for aircraft routes.
    Expects JSON data with 'database_name', 'slider_perc', and 'end_year'.
    """
    data = request.json # Get the JSON data from the request
    database_name = data['database_name']
    slider_perc = data['slider_perc']
    end_year = data['end_year']
    result = h2_demand_ac(database_name, slider_perc, end_year) # Call the h2_demand_ac function to perform the calculation
    return jsonify(result) # Converts the result into a JSON and sends it back to the frontend

@app.route('/h2_demand_gse', methods=['POST'])
def h2_demand_gse_endpoint():
    """
    API endpoint to calculate hydrogen demand for ground support equipment.
    Expects JSON data with 'database_name', 'gse', and 'end_year'.
    """
    data = request.json
    database_name = data['database_name']
    gse = [vehicle['type'] for vehicle in data['gse']]
    end_year = data['end_year']
    result = h2_demand_gse(database_name, gse, end_year)
    return jsonify(result)

@app.route('/h2_demand', methods=['POST'])
def h2_demand_endpoint():
    """
    API endpoint to calculate hydrogen demand for both aircraft and ground support equipment.
    Expects JSON data with 'slider_perc', 'gse', and 'end_year'.
    """
    data = request.json
    slider_perc = data['slider_perc']
    gse = [vehicle['type'] for vehicle in data['gse']]
    end_year = data['end_year']
    
    aircraft_demand = h2_demand_ac('aircraft_data.db', slider_perc, end_year)
    gse_demand = h2_demand_gse('ground_fleet_data.db', gse, end_year)
    
    result = {
        "aircraft_demand": aircraft_demand,
        "gse_demand": gse_demand,
        "total_demand": aircraft_demand + gse_demand["total_h2_demand_vol_gse"]
    }
    return jsonify(result)

@app.route('/economic_impact', methods=['POST'])
def economic_impact_endpoint():
    """
    API endpoint to calculate the economic impact of switching to hydrogen fuel.
    Expects JSON data with 'd', and 'tax_credits'.
    """
    data = request.json
    # d = data['d']
    tax_credits = data['tax_credits']
    # fleetPercentage
    # totalFlights
    # atlantaFraction
    # hydrogenDemand
    # turnaroundTime
    # taxCredits
    result = hydrogen_uti_rev(d, tax_credits)
    return jsonify(result)

@app.route('/storage_cost', methods=['POST'])
def storage_cost_endpoint():
    """
    API endpoint to calculate the storage cost for hydrogen.
    Expects JSON data with 'total_h2_volume_gal', 'number_of_tanks', 'tank_diameter_ft', 
    'tank_length_ft', 'cost_per_sqft_construction', and 'cost_per_cuft_insulation'.
    """
    data = request.json
    total_h2_volume_gal = data['total_h2_volume_gal']
    number_of_tanks = data['number_of_tanks']
    tank_diameter_ft = data['tank_diameter_ft']
    tank_length_ft = data['tank_length_ft']
    cost_per_sqft_construction = data['cost_per_sqft_construction']
    cost_per_cuft_insulation = data['cost_per_cuft_insulation']
    result = calculate_h2_storage_cost(
        total_h2_volume_gal,
        number_of_tanks,
        tank_diameter_ft,
        tank_length_ft,
        cost_per_sqft_construction,
        cost_per_cuft_insulation
    )
    return jsonify(result)

@app.route('/data/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'data'), filename)

if __name__ == '__main__':
    app.run(debug=True)
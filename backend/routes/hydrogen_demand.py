"""API routes for hydrogen demand calculations."""
from flask import Blueprint, request, jsonify
from services.hydrogen_service import (
    calculate_aircraft_hydrogen_demand,
    calculate_gse_hydrogen_demand,
    calculate_total_hydrogen_demand
)

hydrogen_demand_bp = Blueprint('hydrogen_demand', __name__)

@hydrogen_demand_bp.route('/aircraft', methods=['POST'])
def h2_demand_ac_endpoint():
    """Calculate hydrogen demand for aircraft routes."""
    data = request.json
    database_name = data.get('database_name')
    slider_perc = data.get('slider_perc')
    end_year = data.get('end_year')
    
    result = calculate_aircraft_hydrogen_demand(database_name, slider_perc, end_year)
    return jsonify(result)

@hydrogen_demand_bp.route('/gse', methods=['POST'])
def h2_demand_gse_endpoint():
    """Calculate hydrogen demand for ground support equipment."""
    data = request.json
    database_name = data.get('database_name')
    gse = [vehicle['type'] for vehicle in data.get('gse', [])]
    end_year = data.get('end_year')
    
    result = calculate_gse_hydrogen_demand(database_name, gse, end_year)
    return jsonify(result)

@hydrogen_demand_bp.route('/total', methods=['POST'])
def h2_demand_total_endpoint():
    """Calculate total hydrogen demand for both aircraft and GSE."""
    data = request.json
    slider_perc = data.get('slider_perc')
    gse = [vehicle['type'] for vehicle in data.get('gse', [])]
    end_year = data.get('end_year')
    
    result = calculate_total_hydrogen_demand(slider_perc, gse, end_year)
    return jsonify(result)
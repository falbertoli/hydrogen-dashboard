"""API routes for economic impact calculations."""
from flask import Blueprint, request, jsonify
from services.economic_service import calculate_hydrogen_economic_impact

economic_bp = Blueprint('economic', __name__)

@economic_bp.route('/impact', methods=['POST'])
def economic_impact_endpoint():
    """
    API endpoint to calculate the economic impact of switching to hydrogen fuel.
    Expects JSON data with economic parameters.
    """
    data = request.json
    
    fleet_percentage = data.get('fleet_percentage')
    total_flights = data.get('total_flights')
    atlanta_fraction = data.get('atlanta_fraction')
    hydrogen_demand = data.get('hydrogen_demand')
    turnaround_time = data.get('turnaround_time')
    tax_credits = data.get('tax_credits')
    
    result = calculate_hydrogen_economic_impact(
        fleet_percentage,
        total_flights,
        atlanta_fraction,
        hydrogen_demand,
        turnaround_time,
        tax_credits
    )
    return jsonify(result)
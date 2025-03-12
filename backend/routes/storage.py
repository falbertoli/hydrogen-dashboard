"""API routes for hydrogen storage calculations."""
from flask import Blueprint, request, jsonify
from services.storage_service import calculate_h2_storage_cost

storage_bp = Blueprint('storage', __name__)

@storage_bp.route('/calculate', methods=['POST'])
def storage_cost_endpoint():
    """
    API endpoint to calculate the storage cost for hydrogen.
    Expects JSON data with storage parameters.
    """
    data = request.json
    total_h2_volume_gal = data.get('total_h2_volume_gal')
    number_of_tanks = data.get('number_of_tanks')
    tank_diameter_ft = data.get('tank_diameter_ft')
    tank_length_ft = data.get('tank_length_ft')
    cost_per_sqft_construction = data.get('cost_per_sqft_construction')
    cost_per_cuft_insulation = data.get('cost_per_cuft_insulation')
    
    result = calculate_h2_storage_cost(
        total_h2_volume_gal,
        number_of_tanks,
        tank_diameter_ft,
        tank_length_ft,
        cost_per_sqft_construction,
        cost_per_cuft_insulation
    )
    return jsonify(result)
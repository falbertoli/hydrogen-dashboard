# backend/routes/hydrogen_demand.py
from flask import Blueprint, request, jsonify, g, current_app
from services.hydrogen_service import HydrogenService
from repositories.aircraft_repository import AircraftRepository
from repositories.gse_repository import GSERepository
from utils.database import get_aircraft_db_session, get_gse_db_session
from schemas.hydrogen_demand import (
    AircraftDemandQuery, 
    AircraftDemandResult, 
    GSEDemandQuery, 
    TotalDemandQuery
)
from utils.validation import validate_input
import logging

hydrogen_demand_bp = Blueprint('hydrogen_demand', __name__)
logger = logging.getLogger(__name__)

@hydrogen_demand_bp.before_request
def before_request():
    """Establish database connections before each request."""
    try:
        g.aircraft_db = next(get_aircraft_db_session())
        g.gse_db = next(get_gse_db_session())
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return jsonify({"error": "Database connection failed"}), 500

@hydrogen_demand_bp.teardown_request
def teardown_request(exception=None):
    """Close database connections after each request."""
    if exception:
        logger.error(f"Request error: {str(exception)}")
    
    for db_name in ['aircraft_db', 'gse_db']:
        db = getattr(g, db_name, None)
        if db is not None:
            try:
                db.close()
            except Exception as e:
                logger.error(f"Error closing {db_name}: {str(e)}")

def create_hydrogen_service():
    """Create and return a HydrogenService instance with repositories."""
    return HydrogenService(
        AircraftRepository(g.aircraft_db),
        GSERepository(g.gse_db)
    )

@hydrogen_demand_bp.route('/aircraft', methods=['POST'])
def h2_demand_ac_endpoint():
    """Calculate hydrogen demand for aircraft routes."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        validated_data = validate_input(AircraftDemandQuery, data)
        if isinstance(validated_data, tuple):
            return validated_data

        hydrogen_service = create_hydrogen_service()
        result = hydrogen_service.calculate_aircraft_hydrogen_demand(
            validated_data.slider_perc,
            validated_data.end_year
        )

        validated_result = validate_input(
            AircraftDemandResult,
            {"daily_hydrogen_demand_volume": result}
        )
        if isinstance(validated_result, tuple):
            return validated_result

        return jsonify({"daily_hydrogen_demand_volume": result})

    except Exception as e:
        logger.error(f"Error in aircraft demand calculation: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@hydrogen_demand_bp.route('/gse', methods=['POST'])
def h2_demand_gse_endpoint():
    """Calculate hydrogen demand for ground support equipment."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        validated_data = validate_input(GSEDemandQuery, data)
        if isinstance(validated_data, tuple):
            return validated_data

        hydrogen_service = create_hydrogen_service()
        result = hydrogen_service.calculate_gse_hydrogen_demand(
            validated_data.gse,
            validated_data.end_year
        )

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in GSE demand calculation: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@hydrogen_demand_bp.route('/total', methods=['POST'])
def h2_demand_total_endpoint():
    """Calculate total hydrogen demand for both aircraft and GSE."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        validated_data = validate_input(TotalDemandQuery, data)
        if isinstance(validated_data, tuple):
            return validated_data

        hydrogen_service = create_hydrogen_service()
        
        aircraft_demand = hydrogen_service.calculate_aircraft_hydrogen_demand(
            validated_data.slider_perc,
            validated_data.end_year
        )
        
        gse_demand = hydrogen_service.calculate_gse_hydrogen_demand(
            validated_data.gse,
            validated_data.end_year
        )

        result = {
            "aircraft_demand": aircraft_demand,
            "gse_demand": gse_demand,
            "total_demand": aircraft_demand + gse_demand["total_h2_demand_vol_gse"]
        }
        
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in total demand calculation: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
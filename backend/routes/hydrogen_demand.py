# backend/routes/hydrogen_demand.py
from flask import Blueprint, request, jsonify, g
from services.hydrogen_service import HydrogenService
from repositories.aircraft_repository import AircraftRepository
from repositories.gse_repository import GSERepository
from utils.database import get_aircraft_db_session, get_gse_db_session
from schemas.hydrogen_demand import AircraftDemandQuery, AircraftDemandResult, GSEDemandQuery, TotalDemandQuery # Import schemas
from utils.validation import validate_input

hydrogen_demand_bp = Blueprint('hydrogen_demand', __name__)


@hydrogen_demand_bp.before_request
def before_request():
    """Establish database connections before each request."""
    g.aircraft_db = next(get_aircraft_db_session())  # Get a database session
    g.gse_db = next(get_gse_db_session())


@hydrogen_demand_bp.teardown_request
def teardown_request(exception=None):
    """Close database connections after each request."""
    aircraft_db = getattr(g, 'aircraft_db', None)
    gse_db = getattr(g, 'gse_db', None)
    if aircraft_db is not None:
        g.aircraft_db.close()
    if gse_db is not None:
        g.gse_db.close()


@hydrogen_demand_bp.route('/aircraft', methods=['POST'])
def h2_demand_ac_endpoint():
    """Calculate hydrogen demand for aircraft routes."""
    data = request.get_json()
    validated_data = validate_input(AircraftDemandQuery, data)

    if isinstance(validated_data, tuple):  # It's an error
        return validated_data  # Return the error response

    aircraft_repo = AircraftRepository(g.aircraft_db)
    gse_repo = GSERepository(g.gse_db)  #GSE Repo
    hydrogen_service = HydrogenService(aircraft_repo, gse_repo)  # Pass both repos

    result = hydrogen_service.calculate_aircraft_hydrogen_demand(
        validated_data.slider_perc, validated_data.end_year
    )
    validated_result = validate_input(AircraftDemandResult, {"daily_hydrogen_demand_volume": result})
    if isinstance(validated_result, tuple):
        return validated_result

    return jsonify({"daily_hydrogen_demand_volume": result})

@hydrogen_demand_bp.route('/gse', methods=['POST'])
def h2_demand_gse_endpoint():
    """Calculate hydrogen demand for ground support equipment."""
    data = request.get_json()

    validated_data = validate_input(GSEDemandQuery, data)

    if isinstance(validated_data, tuple):  # It's an error
        return validated_data


    aircraft_repo = AircraftRepository(g.aircraft_db)
    gse_repo = GSERepository(g.gse_db)  # GSE Repo
    hydrogen_service = HydrogenService(aircraft_repo, gse_repo)  # Pass both repos

    # Use Hydrogenservice to calculate
    result = hydrogen_service.calculate_gse_hydrogen_demand(
        validated_data.gse, validated_data.end_year
    )

    return jsonify(result)


@hydrogen_demand_bp.route('/total', methods=['POST'])
def h2_demand_total_endpoint():
    """Calculate total hydrogen demand for both aircraft and GSE."""
    data = request.get_json()

    validated_data = validate_input(TotalDemandQuery, data)

    if isinstance(validated_data, tuple):  # It's an error
        return validated_data

    aircraft_repo = AircraftRepository(g.aircraft_db)
    gse_repo = GSERepository(g.gse_db)  # GSE Repo
    hydrogen_service = HydrogenService(aircraft_repo, gse_repo)  # Pass both repos


    aircraft_demand = hydrogen_service.calculate_aircraft_hydrogen_demand(
        validated_data.slider_perc, validated_data.end_year
    )
    gse_demand = hydrogen_service.calculate_gse_hydrogen_demand(
        validated_data.gse, validated_data.end_year
    )

    result = {
        "aircraft_demand": aircraft_demand,
        "gse_demand": gse_demand,
        "total_demand": aircraft_demand + gse_demand["total_h2_demand_vol_gse"]
    }
    return jsonify(result)
# backend/app.py
"""
Hydrogen Dashboard Backend API

This Flask application provides API endpoints for:
1. Hydrogen demand calculations
2. Storage capacity calculations
3. Financial analysis for hydrogen fleet transition

Dependencies:
- Flask: Web framework
- Flask-CORS: Cross-origin resource sharing
- Pandas: Data processing for financial calculations
- NumPy: Numerical calculations
- Pydantic: Input validation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field, ValidationError, ConfigDict
from typing_extensions import Annotated  # Use typing for Python >= 3.9
import os

app = Flask(__name__)
# Configure CORS for development (update origins for production)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Constants (consider moving to config.py for production)
TANK_WIDTH = 10.1667  # ft
TANK_LENGTH = 56.5  # ft
WATER_CAP = 18014 / 7.48052  # gal to ft³
TANK_ULLAGE = 0.05  # 5% volume loss due to ullage
EVAPORATION = 0.9925  # 99.25% LH2 retention per day
H2_DENS = 4.43  # lbs/ft³ (liquid hydrogen density)
SAFETY_DISTANCE = 1000  # ft, minimum distance required from buildings
REVENUE_PER_FLIGHT = 32_599_650 / 500_000  # USD, example revenue per flight

# Load CSV data at startup for financial calculations
try:
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'T_SCHEDULE_T1.csv')
    uti_data = pd.read_csv(csv_path)
    delta_data = uti_data[(uti_data['UNIQUE_CARRIER'] == 'DL') & (uti_data['REGION'] == 'D')]
except FileNotFoundError:
    raise RuntimeError("CSV file not found. Please ensure 'data/T_SCHEDULE_T1.csv' exists.")

# Input validation models using Pydantic
class DemandInput(BaseModel):
    fleetPercentage: Annotated[int, Field(ge=0, le=100)]  # Percentage of fleet using H2 (0-100)
    selectedVehicles: list[dict]  # List of vehicles with type and count
    selectedTimePeriod: str  # Time period (e.g., "7 days")

class StorageInput(BaseModel):
    storageArea: Annotated[int, Field(ge=0)]  # Storage area in sq ft

class FinancialInput(BaseModel):
    # Internal snake_case names with camelCase aliases for frontend compatibility
    fleet_percentage: Annotated[float, Field(ge=0, le=1, alias="fleetPercentage")]  # Fraction of flights changed to H2 (0-1)
    total_flights: Annotated[int, Field(ge=0, alias="totalFlights")]  # Total flights per year
    atlanta_fraction: Annotated[float, Field(ge=0, le=1, alias="atlantaFraction")]  # Fraction of flights from Atlanta
    hydrogen_demand_gal: Annotated[float, Field(ge=0, alias="hydrogenDemand")]  # Hydrogen demand (gallons)
    turnaround_time_min: Annotated[int, Field(ge=0, alias="turnaroundTime")]  # Extra turnaround time (minutes)
    tax_credits_per_gal: Annotated[float, Field(ge=0, alias="taxCredits")]  # Tax credit ($/gal)

    model_config = ConfigDict(
        populate_by_name=True,  # Allow population by alias (camelCase)
        from_attributes=True
    )

def compute_h2_demand(fleet_percentage: int, ground_vehicles: list[dict], time_period: str) -> tuple[float, float]:
    """
    Compute hydrogen demand and required storage volume.

    Args:
        fleet_percentage (int): Percentage of fleet using hydrogen (0-100).
        ground_vehicles (list[dict]): List of hydrogen-powered ground vehicles.
        time_period (str): Time period for demand estimation (e.g., "7 days").

    Returns:
        tuple: (estimated_h2_demand [lbs], storage_needed [ft³])
    """
    try:
        fleet_percentage = int(fleet_percentage)
    except ValueError:
        fleet_percentage = 0

    if not time_period or not time_period.split()[0].isdigit():
        raise ValueError("Invalid time period format. Expected 'X days'.")

    time_multiplier = int(time_period.split()[0])
    demand_factor = 10  # Example factor per fleet percentage
    vehicle_factor = 5  # Example H2 consumption per vehicle

    estimated_h2_demand = (fleet_percentage * demand_factor) + (len(ground_vehicles) * vehicle_factor)
    estimated_h2_demand *= time_multiplier
    storage_needed = estimated_h2_demand / H2_DENS
    return estimated_h2_demand, storage_needed

def get_compliant_areas(required_storage_area: float) -> list[dict]:
    """
    Find airport zones that can accommodate the required storage area.

    Args:
        required_storage_area (float): Required storage area in sq ft.

    Returns:
        list[dict]: List of compliant zones with name, space, and coordinates.
    """
    airport_areas = [
        {
            "name": "Zone 1",
            "space": 500,
            "coordinates": [[33.6405, -84.4265], [33.6405, -84.4295], [33.6425, -84.4295], [33.6425, -84.4265]]
        },
        {
            "name": "Zone 2",
            "space": 1600,
            "coordinates": [[33.6410, -84.4280], [33.6410, -84.4310], [33.6430, -84.4310], [33.6430, -84.4280]]
        },
    ]
    compliant_zones = [area for area in airport_areas if area['space'] >= required_storage_area]
    return compliant_zones

def compute_max_storage(storage_area: int) -> float:
    """
    Compute maximum hydrogen storage for a given area.

    Args:
        storage_area (int): Available storage area in sq ft.

    Returns:
        float: Maximum hydrogen storage in ft³.
    """
    tank_h2_storage = WATER_CAP * (1 - TANK_ULLAGE) * EVAPORATION  # Usable H₂ per tank
    tank_area = TANK_WIDTH * TANK_LENGTH  # Area occupied by one tank
    num_tanks = storage_area / tank_area  # Max tanks in available area
    total_h2_stored = num_tanks * tank_h2_storage  # Total hydrogen stored
    return total_h2_stored

def compute_financial_analysis(data: FinancialInput) -> dict:
    """
    Compute financial metrics for hydrogen fleet transition.

    Args:
        data (FinancialInput): Validated input data.

    Returns:
        dict: Financial metrics including utilization, revenue drop, tax credits, etc.
    """
    A = data.fleet_percentage  # Fraction of flights changed to H2
    B = data.total_flights  # Total flights per year
    C = data.atlanta_fraction  # Fraction of flights from Atlanta
    D = data.hydrogen_demand_gal  # Hydrogen demand (gallons)
    E = data.turnaround_time_min  # Extra turnaround time (minutes)
    tax_credits = data.tax_credits_per_gal  # Tax credit ($/gal)

    # Baseline Jet-A utilization for fraction A and from ATL only
    baseline_jetA_util = A * C * delta_data['REV_ACRFT_HRS_AIRBORNE_610'].sum()

    # Calculate H2 utilization
    utilization_h2 = baseline_jetA_util - (A * B * (E / 60.0))

    # Baseline revenue for fraction A
    baseline_revenue = A * C * REVENUE_PER_FLIGHT / 1_000_000  # Convert to millions USD

    # New revenue from H2 flights
    new_h2_revenue = A * C * REVENUE_PER_FLIGHT * (utilization_h2 / baseline_jetA_util) / 1_000_000

    # Revenue drop
    revenue_drop = baseline_revenue - new_h2_revenue

    # Total tax credits
    total_tax_crd = (D * tax_credits) / 1_000_000

    # Percentage drop in revenue
    pct_drop = 100 * (revenue_drop / baseline_revenue) if baseline_revenue else 0.0

    return {
        "baseline_jetA_utilization": float(baseline_jetA_util),  # hrs/yr
        "hydrogen_utilization": float(utilization_h2),  # hrs/yr
        "baseline_revenue": float(baseline_revenue),  # million USD
        "new_h2_revenue": float(new_h2_revenue),  # million USD
        "revenue_drop": float(revenue_drop),  # million USD
        "total_tax_credits": float(total_tax_crd),  # million USD
        "percent_revenue_drop": float(pct_drop)  # %
    }

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """
    API endpoint for calculations.

    Request Body:
        - calculationMode (str): "demand", "storage", or "financial"
        - Other fields depend on the calculation mode

    Response:
        - success (bool): True if successful, False otherwise
        - data (dict): Calculation results
        - error (str): Error message if applicable
    """
    try:
        data = request.json
        if not data:
            return jsonify({
                "success": False,
                "data": None,
                "error": "Missing request body"
            }), 400

        calc_mode = data.get("calculationMode", "demand")

        if calc_mode == "demand":
            try:
                demand_input = DemandInput(**data)
                h2_demand, storage_needed = compute_h2_demand(
                    demand_input.fleetPercentage,
                    demand_input.selectedVehicles,
                    demand_input.selectedTimePeriod
                )
                compliant_zones = get_compliant_areas(storage_needed)
                response = {
                    "success": True,
                    "data": {
                        "estimatedH2Demand": float(h2_demand),  # lbs
                        "requiredStorageArea": float(storage_needed),  # ft²
                        "storageLocationFound": len(compliant_zones) > 0,
                        "compliantZones": compliant_zones
                    },
                    "error": None
                }
            except ValidationError as e:
                response = {
                    "success": False,
                    "data": None,
                    "error": f"Invalid demand input: {e}"
                }

        elif calc_mode == "storage":
            try:
                storage_input = StorageInput(**data)
                max_h2_stored = compute_max_storage(storage_input.storageArea)
                response = {
                    "success": True,
                    "data": {
                        "maxHydrogenStored": float(max_h2_stored)  # ft³
                    },
                    "error": None
                }
            except ValidationError as e:
                response = {
                    "success": False,
                    "data": None,
                    "error": f"Invalid storage input: {e}"
                }

        elif calc_mode == "financial":
            try:
                financial_input = FinancialInput(**data)
                financial_results = compute_financial_analysis(financial_input)
                response = {
                    "success": True,
                    "data": financial_results,
                    "error": None
                }
            except ValidationError as e:
                response = {
                    "success": False,
                    "data": None,
                    "error": f"Invalid financial input: {e}"
                }

        else:
            response = {
                "success": False,
                "data": None,
                "error": "Invalid calculation mode"
            }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "data": None,
            "error": f"Internal server error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
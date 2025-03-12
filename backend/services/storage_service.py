"""
Service for hydrogen storage calculations.
Contains the business logic for calculating storage costs and requirements.
"""
import numpy as np

def calculate_h2_storage_cost(
    total_h2_volume_gal,        # Total hydrogen volume to store [gallons]
    number_of_tanks,            # Number of tanks
    tank_diameter_ft,           # Diameter of each cylindrical tank [ft]
    tank_length_ft,             # Length of each cylindrical tank [ft]
    cost_per_sqft_construction, # Construction cost [$/ft^2]
    cost_per_cuft_insulation    # Insulation material + manufacturing cost [$/ft^3]
):
    """
    Returns a dictionary of cost estimates for hydrogen storage infrastructure.
    
    Args:
        total_h2_volume_gal: Total hydrogen volume to store [gal].
        number_of_tanks: Number of storage tanks.
        tank_diameter_ft: Diameter of each cylindrical tank [ft].
        tank_length_ft: Length of each cylindrical tank [ft].
        cost_per_sqft_construction: Construction cost in $/ft^2 (footprint).
        cost_per_cuft_insulation: Insulation cost in $/ft^3.
        
    Returns:
        dict: A dictionary with cost breakdown and totals
    """
    # --- 1) Convert total hydrogen volume from gallons to cubic feet
    #         (approx. 1 gal = 0.1337 ft^3)
    total_h2_volume_cuft = total_h2_volume_gal * 0.1337

    # --- 2) Compute the insulation volume for ALL tanks
    h_over_d = tank_length_ft / tank_diameter_ft
    insulation_volume_total = (
        np.pi
        * (tank_diameter_ft / 2.0) ** 2
        * (2.0 * h_over_d - 1.0 / 3.0)
        * (total_h2_volume_cuft / number_of_tanks)
    )

    # --- 3) Insulation cost = total insulation volume × cost per cubic foot
    insulation_cost = insulation_volume_total * cost_per_cuft_insulation

    # --- 4) Footprint calculation
    footprint_per_tank_sqft = tank_diameter_ft * tank_length_ft
    footprint_total = footprint_per_tank_sqft * number_of_tanks

    # --- 5) Construction cost = footprint area × construction cost rate
    construction_cost = footprint_total * cost_per_sqft_construction

    # --- 6) Total infrastructure cost = insulation + construction
    total_infrastructure_cost = insulation_cost + construction_cost

    return {
        "insulation_volume_total": float(insulation_volume_total),
        "insulation_cost": float(insulation_cost),
        "footprint_total": float(footprint_total),
        "construction_cost": float(construction_cost),
        "total_infrastructure_cost": float(total_infrastructure_cost)
    }
"""
This module provides functions to calculate the storage cost for hydrogen.
"""

import numpy as np

def calculate_h2_storage_cost(
    total_h2_volume_gal,
    number_of_tanks,
    tank_diameter_ft,
    tank_length_ft,
    cost_per_sqft_construction,
    cost_per_cuft_insulation
):
    """
    Calculate the storage cost for hydrogen based on the provided parameters.
    """
    total_h2_volume_cuft = total_h2_volume_gal * 0.1337
    h_over_d = tank_length_ft / tank_diameter_ft
    insulation_volume_total = (
        np.pi
        * (tank_diameter_ft / 2.0) ** 2
        * (2.0 * h_over_d - 1.0 / 3.0)
        * (total_h2_volume_cuft / number_of_tanks)
    )
    insulation_cost = insulation_volume_total * cost_per_cuft_insulation
    footprint_per_tank_sqft = tank_diameter_ft * tank_length_ft
    footprint_total = footprint_per_tank_sqft * number_of_tanks
    construction_cost = footprint_total * cost_per_sqft_construction
    total_infrastructure_cost = insulation_cost + construction_cost
    return {
        "insulation_volume_total": insulation_volume_total,
        "insulation_cost": insulation_cost,
        "footprint_total": footprint_total,
        "construction_cost": construction_cost,
        "total_infrastructure_cost": total_infrastructure_cost
    }
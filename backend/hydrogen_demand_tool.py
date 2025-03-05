# backend/hydrogen_demand_tool.py
"""
This module provides functions to calculate hydrogen demand for aircraft routes and ground support equipment.
It interacts with SQLite databases to retrieve and process data.
"""

import pandas as pd
import numpy as np
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def growth_rate_computation(end_year):
    """
    Compute the growth rate for projected operations up to the specified end year.
    """
    growth_rate = pd.DataFrame(GR_DATA)
    delta_part_flights = 0.67
    delta_part_domestic = 0.89

    ops_start = growth_rate.loc[growth_rate["Year"] == 2023, "Projected Operations"].values[0]
    ops_projected = growth_rate.loc[growth_rate["Year"] == end_year, "Projected Operations"].values[0]
    growth = np.divide(ops_projected - ops_start, ops_start)
    growth_delta_atl = growth * delta_part_domestic * delta_part_flights
    return growth_delta_atl

def h2_demand_ac(database_name, slider_perc, end_year):
    """
    Calculate hydrogen demand for aircraft routes.
    """
    conn_ac = sqlite3.connect(f"database/{database_name}")
    query = """
    SELECT "AIR_TIME", "MONTH", "DATA_SOURCE", "FUEL_CONSUMPTION"
    FROM my_table
    WHERE "MONTH" = 7 AND "DATA_SOURCE" = "DU";
    """
    filtered_db = pd.read_sql(query, conn_ac)
    conn_ac.close()
    
    # Remove double quotes from column names
    filtered_db.columns = filtered_db.columns.str.replace('"', '')
    
    filtered_db["AIR_TIME"] = pd.to_numeric(filtered_db["AIR_TIME"], errors='coerce')
    filtered_db["FUEL_CONSUMPTION"] = pd.to_numeric(filtered_db["FUEL_CONSUMPTION"], errors='coerce')

    fuel_weight = 0
    for i in range(len(filtered_db)):
        fuel_weight += filtered_db.iloc[i, 3] * filtered_db.iloc[i, 0] / 60

    fuel_weight_user = slider_perc * fuel_weight
    growth = growth_rate_computation(end_year)
    fuel_weight_projected = fuel_weight_user * (1 + growth)
    conv_factor = 2.8
    h2_weight = fuel_weight_projected / conv_factor
    h2_dens = 4.43
    h2_vol = h2_weight / h2_dens
    buffer = h2_vol / 31
    h2_demand_vol = h2_vol + buffer * 11
    h2_demand_vol_day = h2_demand_vol / 31
    return h2_demand_vol_day

def h2_demand_gse(database_name, gse, end_year):
    """
    Calculate hydrogen demand for ground support equipment.
    
    Args:
        database_name (str): Name of the database file
        gse (list): List of ground support equipment types
        end_year (int): Target year for calculation
    
    Returns:
        dict: Calculation results
    """
    hydrogen_tot_per_cycle = 0
    tot_ops_07 = 33440
    user_input = gse
    placeholders = ', '.join(['?'] * len(user_input))
    conn = sqlite3.connect(f"database/{database_name}")
    query = f"""
    SELECT 
    "Ground support Equipment", 
    "Fuel used", 
    "Usable Fuel Consumption (ft3/min)", 
    "Operating time - Departure", 
    "Operating Time - Arrival"
    FROM my_table
    WHERE "Ground support Equipment" IN ({placeholders});
    """
    file = pd.read_sql(query, conn, params=user_input)
    conn.close()
    
    gse_details = []
    for i in range(len(file)):
        fuel_vol_per_vehicle = (file.iloc[i, 2] * file.iloc[i, 3] + file.iloc[i, 2] * file.iloc[i, 4])
        if file.iloc[i, 1] == "Diesel":
            hydrogen_volume_per_vehicle = fuel_vol_per_vehicle / 2.81
        if file.iloc[i, 1] == "Gasoline":
            hydrogen_volume_per_vehicle = fuel_vol_per_vehicle / 2.76
        hydrogen_tot_per_cycle += hydrogen_volume_per_vehicle
        
        gse_details.append({
            "type": file.iloc[i, 0],
            "fuel_used": file.iloc[i, 1],
            "operating_time_departure": int(file.iloc[i, 3]),
            "operating_time_arrival": int(file.iloc[i, 4]),
            "hydrogen_volume_per_vehicle": float(hydrogen_volume_per_vehicle)
        })

    growth = growth_rate_computation(end_year)
    hydrogen_tot_gse_07 = tot_ops_07 * hydrogen_tot_per_cycle * growth
    buffer = hydrogen_tot_gse_07 / 31
    h2_demand_vol_gse = hydrogen_tot_gse_07 + buffer * 11
    daily_h2_demand_vol_gse = h2_demand_vol_gse / 31
    return {
        "daily_h2_demand_vol_gse": float(daily_h2_demand_vol_gse),
        "total_h2_demand_vol_gse": float(h2_demand_vol_gse),
        "gse_details": gse_details
    }

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

# Growth Rate for each year in a Dataframe - TAF data
GR_DATA = {
    "Year": list(range(2023, 2051)),
    "Projected Operations": [
        755856, 784123, 815016, 834644, 853350, 872286, 890251,
        907846, 925298, 942989, 960976, 979187, 997398, 1016764,
        1036063, 1055234, 1074792, 1094786, 1114237, 1134615, 1155514,
        1176625, 1197973, 1219542, 1241334, 1263264, 1285643, 1308659
    ]
}
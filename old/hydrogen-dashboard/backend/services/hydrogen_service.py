"""
Service for hydrogen demand calculations.
Contains the business logic for calculating hydrogen demand for aircraft and GSE.
"""
import pandas as pd
import numpy as np
import sqlite3
from utils.database import get_db_connection
from constants.hydrogen_properties import GR_DATA

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

def calculate_aircraft_hydrogen_demand(database_name, slider_perc, end_year):
    """
    Calculate hydrogen demand for aircraft routes.
    
    Args:
        database_name (str): Name of the database file
        slider_perc (float): Percentage of fleet to convert to hydrogen
        end_year (int): Target year for calculation
        
    Returns:
        float: Daily hydrogen demand volume
    """
    conn_ac = get_db_connection(database_name)
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

def calculate_gse_hydrogen_demand(database_name, gse, end_year):
    """
    Calculate hydrogen demand for ground support equipment.
    
    Args:
        database_name (str): Name of the database file
        gse (list): List of ground support equipment types
        end_year (int): Target year for calculation
    
    Returns:
        dict: Calculation results with detailed breakdown
    """
    hydrogen_tot_per_cycle = 0
    tot_ops_07 = 33440
    user_input = gse
    placeholders = ', '.join(['?'] * len(user_input))
    conn = get_db_connection(database_name)
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

def calculate_total_hydrogen_demand(slider_perc, gse, end_year):
    """
    Calculate total hydrogen demand for both aircraft and GSE.
    
    Args:
        slider_perc (float): Percentage of aircraft fleet to convert
        gse (list): List of ground support equipment types
        end_year (int): Target year for calculation
        
    Returns:
        dict: Combined calculation results
    """
    from config import AIRCRAFT_DATABASE, GSE_DATABASE
    
    aircraft_demand = calculate_aircraft_hydrogen_demand(AIRCRAFT_DATABASE, slider_perc, end_year)
    gse_demand = calculate_gse_hydrogen_demand(GSE_DATABASE, gse, end_year)
    
    result = {
        "aircraft_demand": aircraft_demand,
        "gse_demand": gse_demand,
        "total_demand": aircraft_demand + gse_demand["total_h2_demand_vol_gse"]
    }
    return result
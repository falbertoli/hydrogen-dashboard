# backend/services/hydrogen_service.py
import pandas as pd
import numpy as np
import logging
from repositories.aircraft_repository import AircraftRepository
from repositories.gse_repository import GSERepository
from constants.hydrogen_properties import GR_DATA, CONVERSION_FACTORS, TANK_SPECS

logger = logging.getLogger(__name__)

class HydrogenService:
    def __init__(self, aircraft_repo: AircraftRepository, gse_repo: GSERepository):
        self.aircraft_repo = aircraft_repo
        self.gse_repo = gse_repo

    def growth_rate_computation(self, end_year):
        """
        Compute growth rate for projected operations.
        
        Logic:
        1. Use TAF data for projected operations
        2. Calculate growth from 2023 to target year
        3. Apply Delta and domestic flight factors
        """
        growth_rate = pd.DataFrame(GR_DATA)
        
        # Get operations for start and end year
        ops_start = growth_rate.loc[growth_rate["Year"] == 2023, "Projected Operations"].values[0]
        ops_projected = growth_rate.loc[growth_rate["Year"] == end_year, "Projected Operations"].values[0]
        
        # Calculate growth and apply factors
        growth = (ops_projected - ops_start) / ops_start
        growth_delta_atl = (growth * 
                           CONVERSION_FACTORS['DELTA_PART_DOMESTIC'] * 
                           CONVERSION_FACTORS['DELTA_PART_FLIGHTS'])
        
        return growth_delta_atl

    def calculate_aircraft_hydrogen_demand(self, slider_perc, end_year):
        """
        Calculate hydrogen demand for aircraft.
        
        Logic:
        1. Get aircraft data for July and domestic flights
        2. Calculate total fuel weight
        3. Apply slider percentage and growth
        4. Convert to hydrogen weight and volume
        5. Add buffer storage
        """
        # Get aircraft data
        aircraft_data = self.aircraft_repo.get_aircraft_data(end_year, slider_perc)
        logger.debug(f"Retrieved {len(aircraft_data)} aircraft records")
        
        if not aircraft_data:
            logger.warning("No aircraft data found")
            return 0.0
        
        # Calculate total fuel weight
        fuel_weight = sum(
            aircraft.fuel_consumption * aircraft.air_time / 60
            for aircraft in aircraft_data
        )
        logger.debug(f"Total fuel weight: {fuel_weight}")
        
        # Apply slider percentage and growth
        fuel_weight_user = slider_perc * fuel_weight
        logger.debug(f"User fuel weight (after slider): {fuel_weight_user}")
        
        growth = self.growth_rate_computation(end_year)
        logger.debug(f"Growth rate: {growth}")
        
        fuel_weight_projected = fuel_weight_user * (1 + growth)
        logger.debug(f"Projected fuel weight: {fuel_weight_projected}")
        
        # Convert to hydrogen
        h2_weight = fuel_weight_projected / CONVERSION_FACTORS['JETA_TO_H2']
        logger.debug(f"H2 weight: {h2_weight}")
        
        h2_vol = h2_weight / CONVERSION_FACTORS['H2_DENSITY']
        logger.debug(f"H2 volume: {h2_vol}")
        
        # Add buffer
        daily_buffer = h2_vol / 31
        h2_demand_vol = h2_vol + (daily_buffer * 11)  # 11 days buffer
        h2_demand_vol_day = h2_demand_vol / 31
        
        logger.debug(f"Daily H2 demand volume: {h2_demand_vol_day}")
        return h2_demand_vol_day

    def calculate_gse_hydrogen_demand(self, gse_types, end_year):
        """
        Calculate hydrogen demand for GSE.
        
        Logic:
        1. Get GSE data for selected equipment
        2. Calculate hydrogen volume per vehicle
        3. Apply growth factor
        4. Add buffer storage
        """
        gse_data = self.gse_repo.get_gse_by_equipment_type(gse_types)
        
        hydrogen_tot_per_cycle = 0
        gse_details = []
        
        for gse in gse_data:
            # Calculate fuel volume per vehicle
            fuel_vol_per_vehicle = (
                gse.usable_fuel_consumption_ft3_min * 
                (gse.operating_time_departure + gse.operating_time_arrival)
            )
            
            # Convert to hydrogen based on fuel type
            if gse.fuel_used == "Diesel":
                hydrogen_volume = fuel_vol_per_vehicle / CONVERSION_FACTORS['DIESEL_TO_H2']
            elif gse.fuel_used == "Gasoline":
                hydrogen_volume = fuel_vol_per_vehicle / CONVERSION_FACTORS['GASOLINE_TO_H2']
            else:
                hydrogen_volume = 0
                
            hydrogen_tot_per_cycle += hydrogen_volume
            
            gse_details.append({
                "type": gse.ground_support_equipment,
                "fuel_used": gse.fuel_used,
                "hydrogen_volume": float(hydrogen_volume)
            })
        
        # Apply growth and calculate total demand
        growth = self.growth_rate_computation(end_year)
        hydrogen_tot_gse = (CONVERSION_FACTORS['TOTAL_OPS_JULY'] * 
                           hydrogen_tot_per_cycle * 
                           (1 + growth))
        
        # Add buffer
        daily_buffer = hydrogen_tot_gse / 31
        h2_demand_vol_gse = hydrogen_tot_gse + (daily_buffer * 11)
        daily_h2_demand_vol_gse = h2_demand_vol_gse / 31
        
        return {
            "daily_h2_demand_vol_gse": float(daily_h2_demand_vol_gse),
            "total_h2_demand_vol_gse": float(h2_demand_vol_gse),
            "gse_details": gse_details
        }

    def calculate_storage_area(self, h2_demand_vol):
        """
        Calculate storage area required for hydrogen demand.
        
        Logic:
        1. Calculate number of tanks needed
        2. Calculate total area based on tank dimensions
        """
        tank_h2_storage = (TANK_SPECS['WATER_CAPACITY'] * 
                          (1 - TANK_SPECS['ULLAGE']) * 
                          TANK_SPECS['EVAPORATION'])
        
        nbr_tanks = h2_demand_vol / tank_h2_storage
        area_tank = TANK_SPECS['WIDTH'] * TANK_SPECS['LENGTH']
        area_tot = area_tank * nbr_tanks
        
        return float(area_tot)
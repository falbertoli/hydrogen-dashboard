# backend/services/hydrogen_service.py
import pandas as pd
import numpy as np
from repositories.aircraft_repository import AircraftRepository
from repositories.gse_repository import GSERepository
from constants.hydrogen_properties import GR_DATA  # Import GR_DATA
from utils.database import get_aircraft_db_session, get_gse_db_session #Import session

class HydrogenService:
    """
    Service for hydrogen demand calculations, utilizing repositories for data access.
    """

    def __init__(self, aircraft_repo: AircraftRepository, gse_repo: GSERepository):
        """
        Initializes the HydrogenService with repositories for aircraft and GSE data.
        """
        self.aircraft_repo = aircraft_repo
        self.gse_repo = gse_repo

    def growth_rate_computation(self, end_year):
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

    def calculate_aircraft_hydrogen_demand(self, slider_perc, end_year):
        """
        Calculate hydrogen demand for aircraft routes using data from the repository.
        """
        aircraft_data = self.aircraft_repo.get_aircraft_data(end_year, slider_perc, limit=None) # Get all records

        fuel_weight = 0
        for aircraft in aircraft_data:
            fuel_weight += aircraft.fuel_consumption * aircraft.air_time / 60

        fuel_weight_user = slider_perc * fuel_weight
        growth = self.growth_rate_computation(end_year)
        fuel_weight_projected = fuel_weight_user * (1 + growth)
        conv_factor = 2.8
        h2_weight = fuel_weight_projected / conv_factor
        h2_dens = 4.43
        h2_vol = h2_weight / h2_dens
        buffer = h2_vol / 31
        h2_demand_vol = h2_vol + buffer * 11
        h2_demand_vol_day = h2_demand_vol / 31
        return h2_demand_vol_day

    def calculate_gse_hydrogen_demand(self, gse_types, end_year):
        """
        Calculate hydrogen demand for ground support equipment using data from the repository.
        """
        gse_data = self.gse_repo.get_gse_by_equipment_type(gse_types)

        hydrogen_tot_per_cycle = 0
        tot_ops_07 = 33440
        gse_details = []

        for gse in gse_data:
            fuel_vol_per_vehicle = (gse.usable_fuel_consumption_ft3_min * gse.operating_time_departure +
                                   gse.usable_fuel_consumption_ft3_min * gse.operating_time_arrival)

            if gse.fuel_used == "Diesel":
                hydrogen_volume_per_vehicle = fuel_vol_per_vehicle / 2.81
            elif gse.fuel_used == "Gasoline":
                hydrogen_volume_per_vehicle = fuel_vol_per_vehicle / 2.76
            else:
                hydrogen_volume_per_vehicle = 0  # Handle other fuel types or unknown cases

            hydrogen_tot_per_cycle += hydrogen_volume_per_vehicle

            gse_details.append({
                "type": gse.ground_support_equipment,
                "fuel_used": gse.fuel_used,
                "operating_time_departure": gse.operating_time_departure,
                "operating_time_arrival": gse.operating_time_arrival,
                "hydrogen_volume_per_vehicle": float(hydrogen_volume_per_vehicle)
            })

        growth = self.growth_rate_computation(end_year)
        hydrogen_tot_gse_07 = tot_ops_07 * hydrogen_tot_per_cycle * growth
        buffer = hydrogen_tot_gse_07 / 31
        h2_demand_vol_gse = hydrogen_tot_gse_07 + buffer * 11
        daily_h2_demand_vol_gse = h2_demand_vol_gse / 31

        return {
            "daily_h2_demand_vol_gse": float(daily_h2_demand_vol_gse),
            "total_h2_demand_vol_gse": float(h2_demand_vol_gse),
            "gse_details": gse_details
        }
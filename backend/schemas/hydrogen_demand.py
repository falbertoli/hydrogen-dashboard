# backend/schemas/hydrogen_demand.py
from pydantic import BaseModel
from typing import List

class AircraftDemandQuery(BaseModel):
   slider_perc: float
   end_year: int

class AircraftDemandResult(BaseModel):
   daily_hydrogen_demand_volume: float

class GSEDemandQuery(BaseModel):
   gse: List[str] #List of GSE types (strings)
   end_year: int

class TotalDemandQuery(BaseModel):
   slider_perc: float
   gse: List[str]
   end_year: int
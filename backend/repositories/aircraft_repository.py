# backend/repositories/aircraft_repository.py
from sqlalchemy.orm import Session
from models.aircraft import Aircraft

class AircraftRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_aircraft_data(self, end_year: int, slider_perc: float, limit: int = 100):
        """Retrieve aircraft data based on filters."""
        return self.db.query(Aircraft).limit(limit).all()  # Returns all Aircraft

    def create_aircraft(self, aircraft_data: dict):
        """Create a new aircraft record."""
        db_aircraft = Aircraft(**aircraft_data)
        self.db.add(db_aircraft)
        self.db.commit()
        self.db.refresh(db_aircraft)
        return db_aircraft
# tests/test_repositories.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.aircraft import Aircraft, Base
from repositories.aircraft_repository import AircraftRepository

# Fixture to create an in-memory SQLite database for testing
@pytest.fixture(scope="function")
def test_db():
    engine = create_engine("sqlite:///:memory:")  # In-memory database
    Base.metadata.create_all(engine)  # Create tables

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Add some sample data
        aircraft1 = Aircraft(departures_performed=1, distance=100, air_time=20, unique_carrier="DL",
                              unique_carrier_name="Delta", origin_airport_id=100, origin="ATL",
                              origin_city_name="Atlanta", dest_airport_id=200, dest="JFK", dest_city_name="New York",
                              aircraft_type=600, month=7, data_source="DU", fuel_consumption=5000)
        aircraft2 = Aircraft(departures_performed=2, distance=200, air_time=40, unique_carrier="UA",
                              unique_carrier_name="United", origin_airport_id=300, origin="ORD",
                              origin_city_name="Chicago", dest_airport_id=400, dest="LAX", dest_city_name="Los Angeles",
                              aircraft_type=700, month=8, data_source="DU", fuel_consumption=6000)
        db.add_all([aircraft1, aircraft2])
        db.commit()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine) # Drop tables after the test

# Test case for AircraftRepository
def test_get_aircraft_data(test_db):
    aircraft_repo = AircraftRepository(test_db)
    aircraft_data = aircraft_repo.get_aircraft_data(end_year=2023, slider_perc=0.5)

    assert len(aircraft_data) == 2
    assert aircraft_data[0].unique_carrier == "DL"
    assert aircraft_data[1].unique_carrier == "UA"

def test_create_aircraft(test_db):
    aircraft_repo = AircraftRepository(test_db)
    new_aircraft_data = {
        "departures_performed": 3,
        "distance": 300,
        "air_time": 60,
        "unique_carrier": "AA",
        "unique_carrier_name": "American Airlines",
        "origin_airport_id": 500,
        "origin": "DFW",
        "origin_city_name": "Dallas",
        "dest_airport_id": 600,
        "dest": "MIA",
        "dest_city_name": "Miami",
        "aircraft_type": 800,
        "month": 9,
        "data_source": "DU",
        "fuel_consumption": 7000,
    }
    new_aircraft = aircraft_repo.create_aircraft(new_aircraft_data)

    assert new_aircraft.unique_carrier == "AA"
    assert new_aircraft.distance == 300
    assert new_aircraft.id is not None  # Check that the ID was assigned
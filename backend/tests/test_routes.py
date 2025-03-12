# tests/test_routes.py
import pytest
import json
import logging
import pandas as pd
from flask import Flask
from models.aircraft import Aircraft, Base as AircraftBase
from models.gse import GroundSupportEquipment, Base as GSEBase
from routes.hydrogen_demand import hydrogen_demand_bp
from utils.database import init_db, get_aircraft_db_session, teardown_db
from config import get_config
from sqlalchemy import create_engine
import os

logger = logging.getLogger(__name__)

def load_test_data():
    """Load a subset of real data for testing."""
    # Load aircraft data
    aircraft_csv_path = os.path.join('data', 'aircraft_data.csv')
    aircraft_data = pd.read_csv(aircraft_csv_path)
    
    # Filter for test data (July and DU)
    test_aircraft_data = aircraft_data[
        (aircraft_data['MONTH'] == 7) & 
        (aircraft_data['DATA_SOURCE'] == 'DU')
    ].head(5)  # Take first 5 rows for testing
    
    # Load GSE data
    gse_csv_path = os.path.join('data', 'gse_data.csv')
    gse_data = pd.read_csv(gse_csv_path, encoding_errors='ignore')
    test_gse_data = gse_data.head(2)  # Take first 2 rows for testing
    
    return test_aircraft_data, test_gse_data

@pytest.fixture(scope="session")
def app():
    """Create test Flask application."""
    config = get_config('testing')
    test_app = Flask(__name__)
    test_app.config.from_object(config)
    
    # Register blueprints
    test_app.register_blueprint(hydrogen_demand_bp, url_prefix='/api/hydrogen-demand')
    
    return test_app

@pytest.fixture(scope="function")
def test_db(app):
    """Set up test database with subset of real data."""
    with app.app_context():
        # Initialize database
        aircraft_engine, gse_engine = init_db(app)
        
        # Load test data from CSV files
        test_aircraft_data, test_gse_data = load_test_data()
        
        # Get session
        db = next(get_aircraft_db_session())
        try:
            # Clear existing data
            db.query(Aircraft).delete()
            
            # Convert DataFrame rows to Aircraft objects
            for _, row in test_aircraft_data.iterrows():
                aircraft = Aircraft(
                    departures_performed=row['DEPARTURES_PERFORMED'],
                    distance=row['DISTANCE'],
                    air_time=row['AIR_TIME'],
                    unique_carrier=row['UNIQUE_CARRIER'],
                    unique_carrier_name=row['UNIQUE_CARRIER_NAME'],
                    origin_airport_id=row['ORIGIN_AIRPORT_ID'],
                    origin=row['ORIGIN'],
                    origin_city_name=row['ORIGIN_CITY_NAME'],
                    dest_airport_id=row['DEST_AIRPORT_ID'],
                    dest=row['DEST'],
                    dest_city_name=row['DEST_CITY_NAME'],
                    aircraft_type=row['AIRCRAFT_TYPE'],
                    month=row['MONTH'],
                    data_source=row['DATA_SOURCE'],
                    fuel_consumption=row['FUEL_CONSUMPTION']
                )
                db.add(aircraft)
            
            db.commit()
            
            # Verify data was inserted
            count = db.query(Aircraft).count()
            logger.debug(f"Inserted {count} aircraft records")
            
            # Print some sample data
            sample = db.query(Aircraft).first()
            if sample:
                logger.debug(f"Sample record: month={sample.month}, "
                           f"source={sample.data_source}, "
                           f"fuel_consumption={sample.fuel_consumption}")
            
            yield db
        finally:
            db.close()
            teardown_db()
            
            # Clean up tables
            AircraftBase.metadata.drop_all(aircraft_engine)
            GSEBase.metadata.drop_all(gse_engine)

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

def test_h2_demand_ac_endpoint(client, app, test_db):
    """Test the /hydrogen-demand/aircraft endpoint."""
    with app.app_context():
        count = test_db.query(Aircraft).count()
        assert count == 5, "Should have 5 test records"
        
        # Verify test data
        aircraft_data = test_db.query(Aircraft).all()
        assert all(a.month == 7 for a in aircraft_data), "All records should be from July"
        assert all(a.data_source == "DU" for a in aircraft_data), "All records should be domestic"
        
        # Calculate expected total fuel weight
        expected_total_fuel = sum(
            a.fuel_consumption * a.air_time / 60 
            for a in aircraft_data
        )
        assert abs(expected_total_fuel - 28574.8) < 0.1, "Total fuel calculation mismatch"
    
    payload = {
        "slider_perc": 0.5,
        "end_year": 2030
    }

    with app.app_context():
        response = client.post('/api/hydrogen-demand/aircraft', json=payload)
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        data = json.loads(response.get_data(as_text=True))
        
        # Verify response structure
        assert "daily_hydrogen_demand_volume" in data
        assert isinstance(data["daily_hydrogen_demand_volume"], float)
        
        # Verify calculation result
        daily_demand = data["daily_hydrogen_demand_volume"]
        assert 56.0 < daily_demand < 57.0, f"Daily demand {daily_demand} outside expected range"
        
        print(f"\nCalculation Summary:")
        print(f"Total Fuel Weight: {expected_total_fuel:.2f} lbs")
        print(f"Daily H2 Demand: {daily_demand:.2f} ft³")

def test_data_loading():
    """Test that we can load the CSV files."""
    aircraft_data, gse_data = load_test_data()
    print("\nAircraft Data Sample:")
    print(aircraft_data.head())
    print("\nGSE Data Sample:")
    print(gse_data.head())
    
    assert not aircraft_data.empty, "Aircraft data should not be empty"
    assert not gse_data.empty, "GSE data should not be empty"
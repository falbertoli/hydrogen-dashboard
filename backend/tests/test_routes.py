# tests/test_routes.py
import pytest
import json
from flask import Flask

from models.aircraft import Aircraft, Base
from routes.hydrogen_demand import hydrogen_demand_bp
from utils.database import init_db, get_aircraft_db_session
from config import get_config

@pytest.fixture(scope="session")
def app():
    """
    Fixture to create a test Flask application.  This is session-scoped so that it is only run once
    :return:
    """
    config = get_config('testing')
    test_app = Flask(__name__)
    test_app.config.from_object(config)

    # Register blueprints
    test_app.register_blueprint(hydrogen_demand_bp, url_prefix='/api/hydrogen-demand')

    # Initialize the database
    with test_app.app_context():
        init_db(test_app)
        engine = test_app.config["SQLALCHEMY_ENGINE"]
        Base.metadata.create_all(engine)
        yield test_app
        Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_client(app):
    """
    Builds a test client
    :param app: App - the application
    :return: a test client
    """
    return app.test_client()


def test_h2_demand_ac_endpoint(test_client):
    """Test the /hydrogen-demand/aircraft endpoint."""
    # Prepare the payload
    payload = {
        "slider_perc": 0.5,
        "end_year": 2030
    }

    # Send a POST request to the endpoint
    response = test_client.post('/api/hydrogen-demand/aircraft', json=payload)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response content type
    assert response.content_type == 'application/json'

    # Parse the JSON response
    data = json.loads(response.get_data(as_text=True))

    # Assert that the response contains the expected data
    assert "daily_hydrogen_demand_volume" in data
    assert isinstance(data["daily_hydrogen_demand_volume"], float)
    assert data["daily_hydrogen_demand_volume"] > 0  # Or any other specific assertion
# tests/test_services.py
import pytest
from unittest.mock import MagicMock

from services.hydrogen_service import HydrogenService
from repositories.aircraft_repository import AircraftRepository
from repositories.gse_repository import GSERepository


@pytest.fixture
def mock_aircraft_repo():
    """Fixture to create a mock AircraftRepository."""
    return MagicMock(spec=AircraftRepository)


@pytest.fixture
def mock_gse_repo():
    """Fixture to create a mock GSERepository."""
    return MagicMock(spec=GSERepository)


@pytest.fixture
def hydrogen_service(mock_aircraft_repo, mock_gse_repo):
    """Fixture to create a HydrogenService instance with mock repositories."""
    return HydrogenService(mock_aircraft_repo, mock_gse_repo)


def test_calculate_aircraft_hydrogen_demand(hydrogen_service, mock_aircraft_repo):
    """Test calculate_aircraft_hydrogen_demand method."""
    # Arrange
    mock_aircraft_repo.get_aircraft_data.return_value = [
        MagicMock(fuel_consumption=5000, air_time=20),
        MagicMock(fuel_consumption=6000, air_time=40),
    ]
    slider_perc = 0.5
    end_year = 2030

    # Act
    result = hydrogen_service.calculate_aircraft_hydrogen_demand(slider_perc, end_year)

    # Assert
    mock_aircraft_repo.get_aircraft_data.assert_called_once_with(end_year, slider_perc, limit=None)
    assert isinstance(result, float)
    assert result > 0  # Add more specific assertions based on your expected output
    # Example of a more specific assertion (you'll need to calculate the expected value):
    # expected_result = ...  # Calculate the expected result based on the mock data
    # assert abs(result - expected_result) < 0.001  # Compare with a tolerance

def test_calculate_aircraft_hydrogen_demand_no_data(hydrogen_service, mock_aircraft_repo):
    """Test calculate_aircraft_hydrogen_demand method when no aircraft data is available."""
    # Arrange
    mock_aircraft_repo.get_aircraft_data.return_value = []  # Simulate no data
    slider_perc = 0.5
    end_year = 2030

    # Act
    result = hydrogen_service.calculate_aircraft_hydrogen_demand(slider_perc, end_year)

    # Assert
    mock_aircraft_repo.get_aircraft_data.assert_called_once_with(end_year, slider_perc, limit=None)
    assert isinstance(result, float)
    assert result == 0.0  # Expect 0.0 when no data is available

def test_calculate_gse_hydrogen_demand(hydrogen_service, mock_gse_repo):
    """Test calculate_gse_hydrogen_demand method."""
    # Arrange
    mock_gse_repo.get_gse_by_equipment_type.return_value = [
        MagicMock(usable_fuel_consumption_ft3_min=0.1, operating_time_departure=10, operating_time_arrival=5, fuel_used="Diesel", ground_support_equipment="Tractor"),
        MagicMock(usable_fuel_consumption_ft3_min=0.2, operating_time_departure=15, operating_time_arrival=10, fuel_used="Gasoline", ground_support_equipment="Belt Loader"),
    ]
    gse_types = ["Tractor", "Belt Loader"]
    end_year = 2030

    # Act
    result = hydrogen_service.calculate_gse_hydrogen_demand(gse_types, end_year)

    # Assert
    mock_gse_repo.get_gse_by_equipment_type.assert_called_once_with(gse_types)
    assert isinstance(result, dict)
    assert "daily_h2_demand_vol_gse" in result
    assert "total_h2_demand_vol_gse" in result
    assert "gse_details" in result
    assert len(result["gse_details"]) == 2
    assert all(isinstance(item, dict) for item in result["gse_details"])

def test_calculate_gse_hydrogen_demand_no_data(hydrogen_service, mock_gse_repo):
    """Test calculate_gse_hydrogen_demand method when no GSE data is available."""
    # Arrange
    mock_gse_repo.get_gse_by_equipment_type.return_value = []
    gse_types = ["Tractor", "Belt Loader"]
    end_year = 2030

    # Act
    result = hydrogen_service.calculate_gse_hydrogen_demand(gse_types, end_year)

    # Assert
    mock_gse_repo.get_gse_by_equipment_type.assert_called_once_with(gse_types)
    assert isinstance(result, dict)
    assert result["daily_h2_demand_vol_gse"] == 0.0
    assert result["total_h2_demand_vol_gse"] == 0.0
    assert result["gse_details"] == []
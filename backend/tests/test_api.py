"""
Basic tests for the restructured API endpoints.
This script will test the main endpoints to ensure they're working correctly.
"""
import requests
import json
import sys
import os

# Add the parent directory to the path so we can import from the backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Base URL for the API
BASE_URL = "http://localhost:5000/api"

def test_hydrogen_demand_aircraft():
    """Test the aircraft hydrogen demand endpoint."""
    url = f"{BASE_URL}/hydrogen-demand/aircraft"
    payload = {
        "database_name": "aircraft_data.db",
        "slider_perc": 0.5,
        "end_year": 2030
    }
    
    response = requests.post(url, json=payload)
    
    print(f"\nTesting {url}")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Response: Success!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_hydrogen_demand_gse():
    """Test the GSE hydrogen demand endpoint."""
    url = f"{BASE_URL}/hydrogen-demand/gse"
    payload = {
        "database_name": "ground_fleet_data.db",
        "gse": [{"type": "Baggage Tractor"}, {"type": "Belt Loader"}],
        "end_year": 2030
    }
    
    response = requests.post(url, json=payload)
    
    print(f"\nTesting {url}")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Response: Success!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_hydrogen_demand_total():
    """Test the total hydrogen demand endpoint."""
    url = f"{BASE_URL}/hydrogen-demand/total"
    payload = {
        "slider_perc": 0.5,
        "gse": [{"type": "Baggage Tractor"}, {"type": "Belt Loader"}],
        "end_year": 2030
    }
    
    response = requests.post(url, json=payload)
    
    print(f"\nTesting {url}")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Response: Success!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_storage_calculate():
    """Test the storage calculation endpoint."""
    url = f"{BASE_URL}/storage/calculate"
    payload = {
        "total_h2_volume_gal": 5000000,
        "number_of_tanks": 20,
        "tank_diameter_ft": 10,
        "tank_length_ft": 40,
        "cost_per_sqft_construction": 580,
        "cost_per_cuft_insulation": 15
    }
    
    response = requests.post(url, json=payload)
    
    print(f"\nTesting {url}")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Response: Success!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_economic_impact():
    """Test the economic impact endpoint."""
    url = f"{BASE_URL}/economic/impact"
    payload = {
        "fleet_percentage": 0.3,
        "total_flights": 100000,
        "atlanta_fraction": 0.4,
        "hydrogen_demand": 5000000,
        "turnaround_time": 30,
        "tax_credits": 0.1
    }
    
    response = requests.post(url, json=payload)
    
    print(f"\nTesting {url}")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Response: Success!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_hydrogen_demand_aircraft,
        test_hydrogen_demand_gse,
        test_hydrogen_demand_total,
        test_storage_calculate,
        test_economic_impact
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n=== Test Results ===")
    for i, result in enumerate(results):
        test_name = tests[i].__name__
        status = "PASSED" if result else "FAILED"
        print(f"{test_name}: {status}")
    
    success_rate = sum(results) / len(results) * 100
    print(f"\nSuccess rate: {success_rate:.2f}%")

if __name__ == "__main__":
    run_all_tests()
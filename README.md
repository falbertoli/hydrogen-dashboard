# Hydrogen Simulation Tool

The Hydrogen Simulation Tool is designed to simulate the hydrogen demand and storage requirements for an airport fleet powered by hydrogen, including both aircraft and ground vehicles. The tool provides estimations of hydrogen demand over specific time periods and calculates the necessary storage infrastructure, factoring in safety regulations and available storage space. Additionally, it integrates financial analysis to assess the economic feasibility of hydrogen infrastructure investments.

## Features

- **Hydrogen Demand Calculation**: Estimate hydrogen demand for aircraft routes and ground support equipment.
- **Storage Cost Calculation**: Calculate the storage cost for hydrogen based on provided parameters.
- **Economic Impact Analysis**: Assess the economic impact of switching to hydrogen fuel, including potential tax incentives.
- **Visualization**: Visualize compliant areas on a map with different colors depending on the level of compliance.

## Technologies Used

- **Backend:** Flask, SQLAlchemy
- **Frontend:** Vue.js, Vuex, Vuetify
- **Database:** SQLite (development), PostgreSQL (production)
- **APIs:** RESTful API with Flask-RESTful

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+

### Backend Setup

1. Navigate to the `backend` directory
   $ cd backend

2. Create a virtual environment and activate it:
   $ python -m venv venv
   $ source venv/Scripts/activate

3. Install the required Python packages:
   $ pip install -r requirements.txt

4. Initialize the databases:
   $ python initialize_db.py

5. Run the Flask application:
   $ python app.py

### Frontend Setup

1. Navigate to the `frontend` directory:
   $ cd frontend

2. Install the required npm packages:
   npm install

3. Run the Vue application:
   $ npm run dev

## Usage

1. Open your web browser and go to `http://localhost:5000` for the Flask backend.
2. Open another tab and go to `http://localhost:8080` for the Vue.js frontend.

## API Endpoints

Hydrogen Demand for Aircraft

- Endpoint: /h2_demand_ac
- Method: POST
- Request Body:
  {
  "database_name": "aircraft_data.db",
  "slider_perc": 0.5,
  "end_year": 2030
  }

Hydrogen Demand for Ground Support Equipment

- Endpoint: /h2_demand_gse
- Method: POST
- Request Body:
  {
  "database_name": "ground_fleet_data.db",
  "gse": ["F250", "F650_1"],
  "end_year": 2030
  }

Economic Impact Analysis

- Endpoint: /economic_impact
- Method: POST
- Request Body:
  {
  "d": 1000,
  "tax_credits": 1.0
  }

Storage Cost Calculation

- Endpoint: /storage_cost
- Method: POST
- Request Body:
  {
  "total_h2_volume_gal": 1000,
  "number_of_tanks": 10,
  "tank_diameter_ft": 20,
  "tank_length_ft": 40,
  "cost_per_sqft_construction": 100,
  "cost_per_cuft_insulation": 50
  }

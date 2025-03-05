"""
This script initializes the SQLite databases by importing data from CSV files.
It reads data from the 'data' folder and populates the databases in the 'database' folder.
"""

import pandas as pd
import sqlite3
import os

def initialize_ac_db():
    """
    Initialize the aircraft data database by importing data from 'aircraft_data.csv'.
    """
    ac_data = pd.read_csv('data/aircraft_data.csv')
    conn = sqlite3.connect("database/aircraft_data.db")
    ac_data.to_sql("my_table", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

def initialize_gse_db():
    """
    Initialize the ground support equipment data database by importing data from 'ground_fleet_data.csv'.
    """
    gse_data = pd.read_csv("data/ground_fleet_data.csv", encoding_errors="ignore")
    conn = sqlite3.connect("database/ground_fleet_data.db")
    gse_data.to_sql("my_table", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

def initialize_economic_db():
    """
    Initialize the economic data database by importing data from 't_schedule_t1.csv'.
    """
    economic_data = pd.read_csv("data/t_schedule_t1.csv")
    conn = sqlite3.connect("database/economic_data.db")
    economic_data.to_sql("my_table", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    os.makedirs("database", exist_ok=True)
    initialize_ac_db()
    initialize_gse_db()
    initialize_economic_db()
    print("Databases initialized successfully.")
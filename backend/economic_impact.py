"""
This module provides functions to calculate the economic impact of switching to hydrogen fuel.
It interacts with SQLite databases to retrieve and process data.
"""

import pandas as pd
import sqlite3

def hydrogen_uti_rev(demand, tax_credits):
    """
    Calculate the economic impact of switching to hydrogen fuel.
    """
    utilization_h2 = (baseline_jet_a_util) - (fraction_h2 * total_flights * (turnaround_time / 60.0))
    baseline_revenue = fraction_h2 * revenue_per_flight * fuel_cost
    new_h2_revenue = fraction_h2 * revenue_per_flight * fuel_cost * (utilization_h2 / baseline_jet_a_util)
    revenue_drop = (baseline_revenue - new_h2_revenue)
    total_tax_credits = ((demand * tax_credits) / 1_000_000)
    return utilization_h2, revenue_drop, total_tax_credits

if __name__ == "__main__":
    conn = sqlite3.connect("database/economic_data.db")
    uti_data = pd.read_sql("SELECT * FROM my_table", conn)
    conn.close()

    fraction_h2 = 0.3
    total_flights = 500_000
    revenue_per_flight = 0.3
    demand = 500 * fraction_h2 * total_flights
    turnaround_time = 30
    tax_credits = 1.0
    delta_data = uti_data[(uti_data['UNIQUE_CARRIER'] == 'DL') & (uti_data['REGION'] == 'D')]
    baseline_jet_a_util = fraction_h2 * revenue_per_flight * delta_data['REV_ACRFT_HRS_AIRBORNE_610'].sum()
    fuel_cost = 32_599_650 / 1_000_000
    utilization_h2, revenue_drop, total_tax_credits = hydrogen_uti_rev(demand, tax_credits)
    print(f"Total flights per year (total_flights) = {total_flights:,}")
    print(f"Fraction to hydrogen (fraction_h2)   = {fraction_h2:.0%}  => # H2 flights = {fraction_h2 * total_flights:,.0f}")
    print(f"Change in turnaround time (turnaround_time) = {turnaround_time:,.0f} mins/flight")
    print(f"\n[1] Baseline Jet-A Utilization (for fraction_h2 for flights from ATL) = {baseline_jet_a_util:,.0f} hrs/yr")
    print(f"[2] Hydrogen utilization (after extra turnaround) = {utilization_h2:,.0f} hrs/yr")
    baseline_revenue = fraction_h2 * revenue_per_flight * fuel_cost
    new_h2_revenue = (fraction_h2 * revenue_per_flight * fuel_cost * (utilization_h2 / baseline_jet_a_util))
    print(f"\n[3] Baseline Jet-A Revenue (for fraction_h2 for flights from ATL) = ${baseline_revenue:,.3f} million")
    print(f"[4] Hydrogen Revenue                     = ${new_h2_revenue :,.3f} million")
    print(f"[5] Total Tax Credits ($/gal)                  = ${total_tax_credits:,.2f}million")
    print(f"\n[6] Drop in Revenue = ${revenue_drop:,.3f} million")
    pct_drop = 100 * (revenue_drop / baseline_revenue) if baseline_revenue else 0.0
    print(f"[7] Percent Drop in Revenue = {pct_drop:.2f}%")
    print("---------------------------------------")
"""
Service for economic impact calculations.
Contains the business logic for calculating economic impacts of hydrogen adoption.
"""
import pandas as pd

def calculate_hydrogen_economic_impact(
    fleet_percentage,     # Fraction of flights changed to hydrogen
    total_flights,        # Total flights per year
    atlanta_fraction,     # Ratio of Delta flights from ATL to total Delta Flights Domestic
    hydrogen_demand,      # Hydrogen demand (gallons)
    turnaround_time,      # Extra turnaround time (minutes) per hydrogen flight
    tax_credits           # Tax credit ($/gal) we might receive or pay
):
    """
    Calculate the economic impact of switching to hydrogen fuel.
    
    Args:
        fleet_percentage: Fraction of flights changed to hydrogen
        total_flights: Total flights per year
        atlanta_fraction: Ratio of flights from ATL to total flights
        hydrogen_demand: Hydrogen demand (gallons)
        turnaround_time: Extra turnaround time (minutes) per hydrogen flight
        tax_credits: Tax credit ($/gal) we might receive or pay
    
    Returns:
        dict: Economic impact metrics
    """
    # These values would typically come from a database or configuration
    # For now, hardcoding them as placeholders
    baseline_jetA_util = 100000  # example value
    total_revenue = 1000000000   # example value
    income_tax = 100000000       # example value
    
    # Calculate H2 utilization
    utilization_h2 = (baseline_jetA_util) - (fleet_percentage * total_flights * (turnaround_time / 60.0))

    # Baseline revenue for the fraction from ATL for domestic flights
    baseline_revenue = fleet_percentage * atlanta_fraction * total_revenue

    # New revenue from H2 flights (scaled by ratio of remaining H2 hours to total hours)
    new_h2_revenue = baseline_revenue * (utilization_h2 / baseline_jetA_util)

    # Total Tax credits 
    total_tax_crd = ((hydrogen_demand * tax_credits) / 1_000_000)

    # Revenue drop = (baseline - new)
    revenue_drop = (baseline_revenue - new_h2_revenue) 

    # Percentage drop in revenue
    pct_drop = 100 * (revenue_drop / baseline_revenue)
    
    # Income tax calculations
    income_tax_portion = (fleet_percentage * income_tax) / 1_000_000
    income_tax_credits = income_tax_portion - total_tax_crd
    
    # Tax credits compensation
    tax_credits_compensation = total_tax_crd - revenue_drop

    return {
        "utilization_h2": float(utilization_h2),
        "baseline_revenue": float(baseline_revenue),
        "new_h2_revenue": float(new_h2_revenue),
        "total_tax_credits": float(total_tax_crd),
        "revenue_drop": float(revenue_drop),
        "percent_drop": float(pct_drop),
        "income_tax": float(income_tax_portion),
        "income_tax_credits": float(income_tax_credits),
        "tax_credits_compensation": float(tax_credits_compensation)
    }
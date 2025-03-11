import pandas as pd
import numpy as np


def hydrogen_uti_rev(A, B, C, D, E, tax_credits):

    # Calculate H2 utilization
    utilization_h2 = (baseline_jetA_util) - (A * B * (E / 60.0))

    # Baseline revenue for the fraction A from ATL for domestic delta flights (F is total annual revenue)
    baseline_revenue = A * C * F

    # New revenue from H2 flights (scaled by ratio of remaining H2 hours to total hours)
    new_h2_revenue = baseline_revenue * (utilization_h2 / baseline_jetA_util)

    # Total Tax credits 
    total_tax_crd = ((D * tax_credits) / 1_000_000)

    # Drop = (baseline - new) minus cost offset from tax credits
    revenue_drop = (baseline_revenue - new_h2_revenue) 

    pct_drop = 100 * (revenue_drop / baseline_revenue)

    return utilization_h2, revenue_drop, total_tax_crd, baseline_revenue, new_h2_revenue, pct_drop


if __name__ == "__main__":

    # ------------------------------------------------------------------
    # 1) Load Data
    # ------------------------------------------------------------------
    uti_data = pd.read_csv('C:/Users/belsa/Documents/GitHub/FLIGHT/Economic/T_SCHEDULE_T1.csv')
    operations_data = pd.read_csv('C:/Users/belsa/Documents/GitHub/FLIGHT/Economic/T_T100D_SEGMENT_US_CARRIER_ONLY.csv')
    #rev_data = pd.read_csv('C:/Users/belsa/Documents/GitHub/FLIGHT/Economic/revenue.csv')
    income_data = pd.read_csv('C:/Users/belsa/Documents/GitHub/FLIGHT/Economic/T_F41SCHEDULE_P12.csv')

    # ------------------------------------------------------------------
    # 2) Filter Data for Delta Airline and Summation
    # ------------------------------------------------------------------
    total_delta_uti = uti_data[
        (uti_data['UNIQUE_CARRIER'] == 'DL') & (uti_data['REGION'] == 'D')
    ]
    atl_delta_oper = operations_data[
        (operations_data['UNIQUE_CARRIER_NAME'] == 'Delta Air Lines Inc.') & (operations_data['ORIGIN'] == 'ATL')
    ]
    total_delta_oper = operations_data[
        (operations_data['UNIQUE_CARRIER_NAME'] == 'Delta Air Lines Inc.')
    ]
    total_revenue = income_data[(income_data['UNIQUE_CARRIER_NAME'] == 'Delta Air Lines Inc.') & (income_data['REGION'] == 'D')]

    #total_income = income_data[(income_data['UNIQUE_CARRIER_NAME'] == 'Delta Air Lines Inc.') & (income_data['REGION'] == 'D')]

    # ------------------------------------------------------------------
    # 3) Define Global Inputs & constants
    # ------------------------------------------------------------------
    # Fraction of flights changed to hydrogen
    A = 0.3
    
    # Total flights per year (so # of hydrogen flights = A*B from hartsfield airport)
    B = total_delta_oper['DEPARTURES_PERFORMED'].sum() # (atl_del_oper) are the total number of domestic flights from atl in an year

    # Ratio of Delta flights from ATL to total Delta Flights Domestic 
    C = atl_delta_oper['DEPARTURES_PERFORMED'].sum()/B
    
    # Hydrogen demand (gallons) (5000 gal Per flight shoud be repalced with value from demand tool) (remove *A*B if using total yearly demand as input)
    D = 2752285.804321897*7.48052*12

    # Extra turnaround time (minutes) per hydrogen flight
    E = 30

    # Tax credit ($/gal) we might receive or pay
    tax_credits = 0.1

    # Jet-A operating revenue for Delta (domestic region), 2024, in millions of USD
    total_revenue = income_data['OP_REVENUES'].sum()/ 1_000_000  # convert to millions
    F = total_revenue

    # Baseline (Jet-A) utilization for fraction A and from ATL only:
    baseline_jetA_util = A * C * total_delta_uti['REV_ACRFT_HRS_AIRBORNE_610'].sum()

    # ------------------------------------------------------------------
    # 4) Compute function 
    # ------------------------------------------------------------------
    utilization_h2, revenue_drop, total_tax_credits, baseline_revenue, new_h2_revenue, pct_drop = hydrogen_uti_rev(A, B, C, D, E, tax_credits)


    # ------------------------------------------------------------------
    # 5) reduced income 
    # ------------------------------------------------------------------
    
    income_tax = (A * income_data['INCOME_TAX'].sum())/1_000_000
    income_tax_credits = income_tax - total_tax_credits

   # ------------------------------------------------------------------
    # 5) reduced income 
    # ------------------------------------------------------------------

    tax_credits_compensation = total_tax_credits - revenue_drop 

    # ------------------------------------------------------------------
    # 7) Print Values
    # ------------------------------------------------------------------

    print("----- Hydrogen Fleet Calculation -----")
    print(f"Total flights per year (B) (All Domestic) = {B:,}")
    print(f"Fraction to hydrogen (A) (from ATL)  = {A:.0%}  => # H2 flights = {A*B*C:,.0f}")
    print(f"Change in turnaround time (E) = {E:,.0f} mins/flight")

    print(f"\n[1] Baseline Jet-A Utilization (for fraction A for flights from ATL) = {baseline_jetA_util:,.0f} hrs/yr")
    print(f"[2] Hydrogen utilization (after extra turnaround) = {utilization_h2:,.0f} hrs/yr")

    print(f"\n[3] Baseline Jet-A Revenue (for fraction A for flights from ATL) = ${baseline_revenue:,.3f} million")
    print(f"[4] Hydrogen Revenue                     = ${new_h2_revenue :,.3f} million")
    print(f"[5] Total Tax Credits ($)                  = ${total_tax_credits:,.2f} million")

    print(f"\n[6] Drop in Revenue = ${revenue_drop:,.3f} million")

    print(f"[7] Percent Drop in Revenue = {pct_drop:.2f}%")
    print(f"[8] Income Tax Without Tax Credits = {income_tax:.2f} million")
    print(f"[9] Income Tax With Tax Credits = {income_tax_credits:.2f} million")
    print(f"[10] Tax Credit Compensation = {tax_credits_compensation:.2f} million")
    print("---------------------------------------")
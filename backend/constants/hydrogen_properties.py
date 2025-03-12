# backend/constants/hydrogen_properties.py
GR_DATA = {
    "Year": list(range(2023, 2051)),
    "Projected Operations": [
        755856, 784123, 815016, 834644, 853350, 872286, 890251, 
        907846, 925298, 942989, 960976, 979187, 997398, 1016764, 
        1036063, 1055234, 1074792, 1094786, 1114237, 1134615, 1155514, 
        1176625, 1197973, 1219542, 1241334, 1263264, 1285643, 1308659
    ]
}

# Constants for calculations
CONVERSION_FACTORS = {
    'DIESEL_TO_H2': 2.81,
    'GASOLINE_TO_H2': 2.76,
    'JETA_TO_H2': 2.8,  # LHV(H2) / LHV(JetA)
    'H2_DENSITY': 4.43,  # lbs/ft3 - Department of Energy for LH2
    'DELTA_PART_FLIGHTS': 0.67,  # Percentage of flights from ATL operated by Delta
    'DELTA_PART_DOMESTIC': 0.89,  # Percentage of Delta ATL flights that are domestic
    'TOTAL_OPS_JULY': 33440  # Total operations during July 2023
}

# Tank specifications
TANK_SPECS = {
    'WIDTH': 10.1667,  # ft
    'LENGTH': 56.5,    # ft
    'WATER_CAPACITY': 18014/7.48052,  # gal->ft3
    'ULLAGE': 0.05,    # % of volume taken by gas form of H2
    'EVAPORATION': 0.9925  # % of LH2 retained per day
}
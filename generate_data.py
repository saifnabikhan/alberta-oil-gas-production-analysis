"""
generate_data.py
----------------
Generates a synthetic Alberta oil and gas production dataset structured
to mirror Alberta Energy Regulator (AER) conventional volumetrics reporting.

Usage:
    python3 generate_data.py

Output:
    alberta_og_production.csv

Dependencies:
    Python 3.x standard library only (csv, random)

Random seed is fixed at 42 for full reproducibility.
See DATA_GENERATION.md for full documentation of modelling assumptions.
"""

import csv
import random

# Fixed seed for reproducibility
random.seed(42)

# -----------------------------------------------------------------------
# Region parameters
# oil_base / gas_base: monthly base production volumes
# well_base: base active well count
# decline: monthly decline rate (annual rates converted to monthly)
# -----------------------------------------------------------------------
regions = {
    "Peace River": {
        "oil_base": 4200,
        "gas_base": 7800,
        "well_base": 175,
        "decline": 0.996,       # ~4.8% annual decline
    },
    "Athabasca": {
        "oil_base": 9500,
        "gas_base": 2800,
        "well_base": 310,
        "decline": 0.998,       # ~2.4% annual decline (oil sands stable)
    },
    "Cold Lake": {
        "oil_base": 7200,
        "gas_base": 2200,
        "well_base": 245,
        "decline": 0.994,       # ~7.2% annual decline
    },
    "Central Alberta": {
        "oil_base": 2800,
        "gas_base": 13500,
        "well_base": 135,
        "decline": 0.991,       # ~10.8% annual decline (mature gas basin)
    },
    "Southern Alberta": {
        "oil_base": 1200,
        "gas_base": 16000,
        "well_base": 85,
        "decline": 0.988,       # ~14.4% annual decline (declining gas basin)
    },
}

# -----------------------------------------------------------------------
# Facility type multipliers
# Reflect real production characteristics of each facility type in Alberta
# -----------------------------------------------------------------------
facility_types = {
    "Battery": {
        "oil_mult": 1.2,
        "gas_mult": 0.9,
        # Conventional oil gathering and separation — oil dominant
    },
    "Gas Plant": {
        "oil_mult": 0.35,
        "gas_mult": 3.1,
        # Gas processing dominant — high gas, low oil
    },
    "Oil Sands Facility": {
        "oil_mult": 2.8,
        "gas_mult": 0.25,
        # SAGD/CSS thermal operations — very high oil, minimal gas
    },
    "Pipeline Terminal": {
        "oil_mult": 0.75,
        "gas_mult": 1.6,
        # Transmission receipt point — mixed volumes
    },
    "Compressor Station": {
        "oil_mult": 0.5,
        "gas_mult": 2.4,
        # Gas compression and forwarding — gas dominant
    },
}

# -----------------------------------------------------------------------
# Operators — fictional names, one assigned per region
# -----------------------------------------------------------------------
operators_by_region = {
    "Peace River":      ["Crestwood Energy Ltd",     "Ridgeline Oil Corp",      "Pemberton Resources Inc"],
    "Athabasca":        ["Lakeland Petroleum Ltd",   "Northland Energy Corp",   "Suncrest Oil Inc"],
    "Cold Lake":        ["Clearwater Production Ltd", "Prairie Basin Resources", "Vermilion Fields Corp"],
    "Central Alberta":  ["Foothills Gas Co",          "Ridgeline Oil Corp",      "Crestwood Energy Ltd"],
    "Southern Alberta": ["Foothills Gas Co",          "Prairie Basin Resources", "Pemberton Resources Inc"],
}

# -----------------------------------------------------------------------
# Seasonal multipliers by month
# Reflect Alberta operational reality:
# - Winter months: reduced due to freeze-up and field access
# - Summer months: peak operations
# -----------------------------------------------------------------------
seasonal = {
    1: 0.87,   # January  — deep freeze
    2: 0.89,   # February — continued winter
    3: 0.94,   # March    — early spring
    4: 0.98,   # April    — spring breakup
    5: 1.03,   # May      — post-breakup recovery
    6: 1.06,   # June     — summer peak begins
    7: 1.09,   # July     — peak operations
    8: 1.07,   # August   — late summer
    9: 1.04,   # September — fall transition
    10: 1.01,  # October  — stable fall
    11: 0.95,  # November — early winter
    12: 0.90,  # December — freeze-up and holiday period
}

# -----------------------------------------------------------------------
# Generate rows
# One row per unique Production_Month + Region + Facility_Type combination
# -----------------------------------------------------------------------
rows = []

for year in range(2020, 2025):
    for month in range(1, 13):
        prod_month = f"{year}-{month:02d}-01"
        months_elapsed = (year - 2020) * 12 + (month - 1)
        season_mult = seasonal[month]

        for region, rp in regions.items():
            # Exponential decline applied cumulatively from Jan 2020
            decline_factor = rp["decline"] ** months_elapsed

            # Rotate operators deterministically (not random) for consistency
            operator = operators_by_region[region][month % 3]

            for facility, fp in facility_types.items():
                # Small random noise to avoid perfectly smooth numbers
                noise = random.uniform(0.93, 1.07)

                oil_vol = round(
                    rp["oil_base"] * fp["oil_mult"]
                    * decline_factor * season_mult * noise, 1
                )
                gas_vol = round(
                    rp["gas_base"] * fp["gas_mult"]
                    * decline_factor * season_mult * noise, 1
                )
                # Water-to-oil ratio: 1.6x to 3.2x oil volume (realistic WOR range)
                water_vol = round(oil_vol * random.uniform(1.6, 3.2), 1)

                # Well count declines with production
                well_count = max(1, int(
                    rp["well_base"] * fp["oil_mult"]
                    * decline_factor * random.uniform(0.95, 1.05)
                ))

                # Uptime: 660–744 hours/month (reflects planned and unplanned downtime)
                uptime = round(random.uniform(660, 744), 1)

                rows.append({
                    "Production_Month":  prod_month,
                    "Region":            region,
                    "Facility_Type":     facility,
                    "Operator":          operator,
                    "Oil_Volume_m3":     oil_vol,
                    "Gas_Volume_e3m3":   gas_vol,
                    "Water_Volume_m3":   water_vol,
                    "Active_Well_Count": well_count,
                    "Uptime_Hours":      uptime,
                })

# -----------------------------------------------------------------------
# Write to CSV
# -----------------------------------------------------------------------
output_file = "alberta_og_production.csv"
with open(output_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> {output_file}")
print(f"Coverage: {rows[0]['Production_Month']} to {rows[-1]['Production_Month']}")
print(f"Regions: {len(set(r['Region'] for r in rows))}")
print(f"Facility types: {len(set(r['Facility_Type'] for r in rows))}")

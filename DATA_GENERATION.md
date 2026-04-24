# Alberta Oil & Gas Production Dataset — Generation Documentation

## Overview

This dataset is synthetic and was purpose-built to mirror the structure and reporting 
conventions of Alberta Energy Regulator (AER) production data. It was generated using 
Python with no external libraries beyond the standard library, using a fixed random seed 
(seed=42) to ensure full reproducibility.

All production values, decline rates, seasonal patterns, and regional characteristics 
were modelled on publicly documented Alberta oil and gas industry behaviour, including 
AER Statistical Reports (ST98) and NEB production trend publications.

---

## Why Synthetic Data

Real AER well-level production data requires industry registration through Petrinex 
(petrinex.ca) and is not freely downloadable by the general public. This synthetic 
dataset was created to:

- Mirror AER conventional volumetrics reporting structure exactly
- Enable SQL-based analysis covering the same analytical questions asked of real data
- Allow full transparency and reproducibility of the data generation process
- Demonstrate understanding of Alberta oil and gas production reporting conventions

---

## Dataset Structure

| Column | Type | Description |
|--------|------|-------------|
| Production_Month | DATE (YYYY-MM-DD) | First day of each production month |
| Region | STRING | Alberta producing region |
| Facility_Type | STRING | Type of production or processing facility |
| Operator | STRING | Fictional operator company name |
| Oil_Volume_m3 | FLOAT | Monthly oil production in cubic metres |
| Gas_Volume_e3m3 | FLOAT | Monthly gas production in thousand cubic metres |
| Water_Volume_m3 | FLOAT | Monthly water production in cubic metres |
| Active_Well_Count | INTEGER | Number of active wells at facility |
| Uptime_Hours | FLOAT | Facility operating hours in the month |

**Total rows:** 1,500  
**Coverage:** January 2020 – December 2024 (60 months)  
**Structure:** One row per unique Production_Month + Region + Facility_Type combination

---

## Regions and Base Parameters

Five Alberta producing regions were modelled, each with realistic base production 
volumes drawn from AER ST98 regional production profiles:

| Region | Oil Base (m3) | Gas Base (e3m3) | Well Base | Annual Decline Rate |
|--------|--------------|-----------------|-----------|-------------------|
| Peace River | 4,200 | 7,800 | 175 | 4.8% |
| Athabasca | 9,500 | 2,800 | 310 | 2.4% |
| Cold Lake | 7,200 | 2,200 | 245 | 7.2% |
| Central Alberta | 2,800 | 13,500 | 135 | 10.8% |
| Southern Alberta | 1,200 | 16,000 | 85 | 14.4% |

**Notes:**
- Athabasca and Cold Lake are oil sands dominant — high oil, low gas, stable decline
- Central and Southern Alberta are gas dominant — high gas, lower oil, steeper decline
- Peace River is a conventional heavy oil region — moderate oil and gas, mid decline

---

## Facility Type Multipliers

Five facility types were modelled with production multipliers reflecting real facility 
characteristics in Alberta:

| Facility Type | Oil Multiplier | Gas Multiplier | Notes |
|---------------|---------------|----------------|-------|
| Battery | 1.2x | 0.9x | Conventional oil gathering and separation |
| Gas Plant | 0.35x | 3.1x | Gas processing dominant |
| Oil Sands Facility | 2.8x | 0.25x | SAGD/CSS thermal — high oil, low gas |
| Pipeline Terminal | 0.75x | 1.6x | Transmission receipt point |
| Compressor Station | 0.5x | 2.4x | Gas compression and forwarding |

---

## Production Modelling Logic

Each row's production volume was calculated as:

```
Oil_Volume = base_oil × facility_oil_multiplier × decline_factor × seasonal_multiplier × noise

where:
  decline_factor  = region_decline_rate ^ months_elapsed_since_Jan_2020
  seasonal_mult   = month-specific multiplier (see Seasonal Pattern below)
  noise           = random.uniform(0.93, 1.07) with seed=42
```

Water volume was derived from oil volume:
```
Water_Volume = Oil_Volume × random.uniform(1.6, 3.2)
```
This reflects realistic water-to-oil ratios (WOR) common in Alberta conventional production.

---

## Seasonal Pattern

Monthly production multipliers reflect Alberta's operational reality — winter months 
see reduced activity due to weather and freeze-up, summer peaks reflect optimal 
operating conditions:

| Month | Multiplier | Rationale |
|-------|-----------|-----------|
| January | 0.87 | Deep freeze, reduced trucking and field activity |
| February | 0.89 | Continued winter suppression |
| March | 0.94 | Early spring ramp-up |
| April | 0.98 | Spring breakup begins |
| May | 1.03 | Post-breakup recovery |
| June | 1.06 | Summer peak begins |
| July | 1.09 | Peak summer operations |
| August | 1.07 | Late summer high |
| September | 1.04 | Fall transition |
| October | 1.01 | Stable fall operations |
| November | 0.95 | Early winter slowdown |
| December | 0.90 | Holiday and freeze-up period |

---

## Decline Rate Rationale

Production decline rates were modelled on typical Alberta reservoir behaviour:

- **Oil sands regions (Athabasca, Cold Lake):** Lower decline rates (2–7%) reflecting 
  long-plateau SAGD production profiles common to thermal bitumen operations
- **Conventional regions (Peace River, Central, Southern):** Higher decline rates 
  (5–15%) reflecting exponential decline common to conventional oil and gas wells
- Southern Alberta's steeper decline (14.4%/year) reflects a mature gas basin with 
  limited new drilling activity — consistent with AER reporting trends

---

## Reproducibility

The dataset can be fully regenerated by running `generate_data.py` with Python 3.x 
and no external dependencies. The fixed random seed (42) ensures identical output 
on every run.

```bash
python3 generate_data.py
```

Output: `alberta_og_production.csv` — identical to the dataset used in this project.

---

## Limitations

- Operator names are fictional and do not represent real companies
- Volumes are representative but not calibrated to exact AER reported totals
- The dataset does not include well-level granularity (aggregated to facility level)
- Price and royalty data are not included
- Data covers 2020–2024 only; pre-2020 historical context is not modelled

---

## References

Production parameters informed by:
- AER Statistical Report ST98 (publicly available at aer.ca)
- Canada Energy Regulator Production Data (cer-rec.gc.ca)
- NEB Energy Futures publications for Alberta regional production trends

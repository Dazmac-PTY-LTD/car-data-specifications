# Car Data Specifications

Comprehensive vehicle specification database sourced from the [auto-data.net](https://auto-data.net) API.

## Dataset Overview

| Metric | Count |
|--------|-------|
| Brands | 391 |
| Models | 3,885 |
| Generations | 10,712 |
| Specifications | 56,885 |

Last fetched: 2026-06-30

## Repository Structure

```
data/
  brands_index.json        — All brands with model counts
  last_fetch.json          — Fetch timestamp and record counts
  brands/                  — Per-brand JSON files (one per manufacturer)
    Toyota.json
    BMW.json
    ...
  flat/
    modifications.csv      — All 56,885 specs in a single flat CSV
scripts/
  fetch.py                 — Re-fetch data from API and regenerate all files
  query.py                 — CLI tool for filtering and searching specs
```

## Data Fields

Each vehicle specification (`modification`) contains:

| Field | Description |
|-------|-------------|
| `id` | Unique modification ID |
| `brand` | Manufacturer name |
| `model` | Model name |
| `generation` | Generation name |
| `model_year` | Generation start year |
| `engine` | Engine descriptor (e.g. `2.0 TDI 150 Hp`) |
| `powertrain` | Drivetrain type (Internal Combustion, Electric, Hybrid, etc.) |
| `power_hp` | Peak power in horsepower |
| `power_rpm` | RPM at peak power |
| `fuel` | Fuel type (Petrol, Diesel, Electric, Hybrid…) |
| `body_style` | Body style (Sedan, SUV, Cabriolet, Coupe…) |
| `seats` | Seating capacity |
| `year_start` | Production start year |
| `year_stop` | Production end year |
| `length_mm` | Vehicle length in mm |
| `width_mm` | Vehicle width in mm |
| `height_mm` | Vehicle height in mm |
| `curb_weight_kg` | Kerb weight in kg |
| `last_updated` | Record last updated timestamp |

## Usage

### Query the flat CSV

```bash
# All Toyota models
python3 scripts/query.py --brand Toyota

# BMW with 300+ HP
python3 scripts/query.py --brand BMW --min-hp 300

# Electric vehicles
python3 scripts/query.py --fuel Electric --limit 50

# SUVs made in 2020
python3 scripts/query.py --body SUV --year 2020

# Toyota Camry specifically
python3 scripts/query.py --brand Toyota --model Camry
```

### Read a brand file directly

```python
import json

with open('data/brands/Toyota.json') as f:
    toyota = json.load(f)

for model in toyota['models']['model']:
    print(model['name'])
```

### Load the full flat CSV in Python

```python
import csv

with open('data/flat/modifications.csv') as f:
    specs = list(csv.DictReader(f))

# Filter EVs over 400 HP
evs = [s for s in specs if 'Electric' in s['fuel'] and s['power_hp'] and int(s['power_hp']) >= 400]
```

### Load in pandas

```python
import pandas as pd

df = pd.read_csv('data/flat/modifications.csv')
print(df.groupby('brand')['power_hp'].max().sort_values(ascending=False).head(10))
```

## Updating Data

To re-fetch the latest data from the API and regenerate all files:

```bash
python3 scripts/fetch.py
```

Requires Python 3.7+ with no external dependencies.

## Data Source

Data sourced from [auto-data.net](https://auto-data.net) API. All vehicle specifications are their property.

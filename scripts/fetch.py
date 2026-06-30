#!/usr/bin/env python3
"""
Fetch latest car specification data from auto-data.net API and regenerate all data files.

Usage:
    python3 scripts/fetch.py

Requires: Python 3.7+, no external dependencies.
"""

import json
import csv
import os
import urllib.request
from datetime import datetime

API_URL = "https://api.auto-data.net/?code=ff622723edf06601f490f1d300cc8ee1&format=json"

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
BRANDS_DIR = os.path.join(DATA_DIR, 'brands')
FLAT_DIR = os.path.join(DATA_DIR, 'flat')


def fetch_data():
    print(f"Fetching data from API...")
    with urllib.request.urlopen(API_URL) as response:
        raw = response.read()
    print(f"Downloaded {len(raw):,} bytes")
    return json.loads(raw)


def write_brand_files(brands):
    os.makedirs(BRANDS_DIR, exist_ok=True)
    for brand in brands:
        safe_name = brand['name'].replace('/', '-').replace(' ', '_')
        path = os.path.join(BRANDS_DIR, f"{safe_name}.json")
        with open(path, 'w') as f:
            json.dump(brand, f, indent=2)
    print(f"Written {len(brands)} brand files to data/brands/")


def write_brands_index(brands):
    index = [
        {
            'id': b['id'],
            'name': b['name'],
            'model_count': len(b['models']['model']),
            'updated': b['update'],
        }
        for b in brands
    ]
    path = os.path.join(DATA_DIR, 'brands_index.json')
    with open(path, 'w') as f:
        json.dump(index, f, indent=2)
    print(f"Written brands_index.json ({len(index)} brands)")


def write_flat_csv(brands):
    os.makedirs(FLAT_DIR, exist_ok=True)
    rows = []
    for brand in brands:
        for model in brand['models']['model']:
            for gen in model['generations']['generation']:
                for mod in gen['modifications']['modification']:
                    rows.append({
                        'id':            mod.get('id', ''),
                        'brand':         mod.get('brand', ''),
                        'model':         mod.get('model', ''),
                        'generation':    mod.get('generation', ''),
                        'model_year':    gen.get('modelYear', ''),
                        'engine':        mod.get('engine', ''),
                        'powertrain':    mod.get('powertrain', ''),
                        'power_hp':      mod.get('powerHp', ''),
                        'power_rpm':     mod.get('powerRpm', ''),
                        'fuel':          mod.get('fuel', ''),
                        'body_style':    mod.get('coupe', ''),
                        'seats':         mod.get('places', ''),
                        'year_start':    mod.get('yearstart', ''),
                        'year_stop':     mod.get('yearstop', ''),
                        'length_mm':     mod.get('length', ''),
                        'width_mm':      mod.get('width', ''),
                        'height_mm':     mod.get('height', ''),
                        'curb_weight_kg': mod.get('curbWeight', ''),
                        'last_updated':  mod.get('update', ''),
                    })

    path = os.path.join(FLAT_DIR, 'modifications.csv')
    fields = list(rows[0].keys())
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Written modifications.csv ({len(rows):,} rows)")


def write_fetch_log(brands):
    brands_count = len(brands)
    models_count = sum(len(b['models']['model']) for b in brands)
    gens_count = sum(len(m['generations']['generation']) for b in brands for m in b['models']['model'])
    mods_count = sum(
        len(g['modifications']['modification'])
        for b in brands
        for m in b['models']['model']
        for g in m['generations']['generation']
    )
    log = {
        'fetched_at': datetime.utcnow().isoformat() + 'Z',
        'brands': brands_count,
        'models': models_count,
        'generations': gens_count,
        'modifications': mods_count,
    }
    path = os.path.join(DATA_DIR, 'last_fetch.json')
    with open(path, 'w') as f:
        json.dump(log, f, indent=2)
    print(f"Stats: {brands_count} brands, {models_count} models, {gens_count} generations, {mods_count} modifications")


def main():
    data = fetch_data()
    brands = data['brands']['brand']
    write_brand_files(brands)
    write_brands_index(brands)
    write_flat_csv(brands)
    write_fetch_log(brands)
    print("Done.")


if __name__ == '__main__':
    main()

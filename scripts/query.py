#!/usr/bin/env python3
"""
Query the car specifications data.

Usage examples:
    python3 scripts/query.py --brand Toyota
    python3 scripts/query.py --brand Toyota --model Camry
    python3 scripts/query.py --fuel Electric
    python3 scripts/query.py --year 2020 --body Sedan
    python3 scripts/query.py --brand BMW --min-hp 300
"""

import json
import csv
import os
import argparse

FLAT_CSV = os.path.join(os.path.dirname(__file__), '..', 'data', 'flat', 'modifications.csv')


def load_data():
    with open(FLAT_CSV, newline='') as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser(description='Query car specification data')
    parser.add_argument('--brand',   help='Filter by brand name (partial match, case-insensitive)')
    parser.add_argument('--model',   help='Filter by model name (partial match, case-insensitive)')
    parser.add_argument('--fuel',    help='Filter by fuel type (e.g. Electric, Petrol, Diesel, Hybrid)')
    parser.add_argument('--body',    help='Filter by body style (e.g. Sedan, SUV, Cabriolet, Coupe)')
    parser.add_argument('--year',    type=int, help='Filter by production year (within yearstart-yearstop range)')
    parser.add_argument('--min-hp',  type=int, help='Minimum horsepower')
    parser.add_argument('--max-hp',  type=int, help='Maximum horsepower')
    parser.add_argument('--limit',   type=int, default=20, help='Max results to show (default 20)')
    args = parser.parse_args()

    rows = load_data()

    if args.brand:
        rows = [r for r in rows if args.brand.lower() in r['brand'].lower()]
    if args.model:
        rows = [r for r in rows if args.model.lower() in r['model'].lower()]
    if args.fuel:
        rows = [r for r in rows if args.fuel.lower() in r['fuel'].lower()]
    if args.body:
        rows = [r for r in rows if args.body.lower() in r['body_style'].lower()]
    if args.year:
        def in_range(r):
            try:
                return int(r['year_start']) <= args.year <= (int(r['year_stop']) if r['year_stop'] else 9999)
            except (ValueError, TypeError):
                return False
        rows = [r for r in rows if in_range(r)]
    if args.min_hp:
        rows = [r for r in rows if r['power_hp'] and int(r['power_hp']) >= args.min_hp]
    if args.max_hp:
        rows = [r for r in rows if r['power_hp'] and int(r['power_hp']) <= args.max_hp]

    print(f"Found {len(rows)} results (showing up to {args.limit})\n")
    for r in rows[:args.limit]:
        print(f"[{r['id']}] {r['brand']} {r['model']} {r['generation']}")
        print(f"      Engine: {r['engine']}  |  Fuel: {r['fuel']}  |  Body: {r['body_style']}")
        print(f"      Years: {r['year_start']}-{r['year_stop']}  |  HP: {r['power_hp']}  |  Weight: {r['curb_weight_kg']} kg")
        print()


if __name__ == '__main__':
    main()

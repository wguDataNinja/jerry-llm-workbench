#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

SELECTED_COLUMNS = [
    'status',
    'price',
    'bed',
    'bath',
    'acre_lot',
    'city',
    'state',
    'zip_code',
    'house_size',
    'prev_sold_date',
    'price_band',
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Create a compact experiment input CSV from a sample CSV.'
    )
    parser.add_argument('--input-csv', required=True)
    parser.add_argument('--output-csv', required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_csv)
    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f'Input CSV not found: {input_path}')

    with input_path.open('r', encoding='utf-8', newline='') as src:
        reader = csv.DictReader(src)
        missing = [c for c in SELECTED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f'Missing expected columns: {missing}')

        out_fields = ['listing_id'] + SELECTED_COLUMNS
        with output_path.open('w', encoding='utf-8', newline='') as dst:
            writer = csv.DictWriter(dst, fieldnames=out_fields)
            writer.writeheader()
            for idx, row in enumerate(reader, start=1):
                out = {'listing_id': f'32092-sold-{idx:03d}'}
                for col in SELECTED_COLUMNS:
                    out[col] = (row.get(col) or '').strip()
                writer.writerow(out)

    print(f'Wrote experiment input CSV: {output_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

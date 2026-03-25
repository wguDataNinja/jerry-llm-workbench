#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import median


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Compare benchmark runs using run manifest and output CSVs.'
    )
    parser.add_argument(
        '--manifest-csv',
        default='experiments/listing_summary__kaggle_usa_real_estate_dataset/results/run_manifest.csv',
    )
    parser.add_argument(
        '--output-csv',
        default='experiments/listing_summary__kaggle_usa_real_estate_dataset/results/run_comparison.csv',
    )
    return parser.parse_args()


def word_count(text: str) -> int:
    return len((text or '').strip().split())


def summarize_output_csv(path: Path) -> dict[str, str]:
    if not path.exists():
        return {
            'output_exists': 'no',
            'output_rows': '0',
            'nonempty_summary_pct': '0.00',
            'avg_summary_words': '0.00',
            'median_summary_words': '0.00',
            'low_rows': '0',
            'mid_rows': '0',
            'high_rows': '0',
        }

    rows = []
    with path.open('r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return {
            'output_exists': 'yes',
            'output_rows': '0',
            'nonempty_summary_pct': '0.00',
            'avg_summary_words': '0.00',
            'median_summary_words': '0.00',
            'low_rows': '0',
            'mid_rows': '0',
            'high_rows': '0',
        }

    words = [word_count(r.get('summary_text', '')) for r in rows]
    nonempty = sum(1 for w in words if w > 0)
    low_rows = sum(1 for r in rows if (r.get('price_band', '') or '').strip() == 'low')
    mid_rows = sum(1 for r in rows if (r.get('price_band', '') or '').strip() == 'mid')
    high_rows = sum(1 for r in rows if (r.get('price_band', '') or '').strip() == 'high')

    return {
        'output_exists': 'yes',
        'output_rows': str(len(rows)),
        'nonempty_summary_pct': f'{(nonempty / len(rows)) * 100:.2f}',
        'avg_summary_words': f'{sum(words) / len(words):.2f}',
        'median_summary_words': f'{median(words):.2f}',
        'low_rows': str(low_rows),
        'mid_rows': str(mid_rows),
        'high_rows': str(high_rows),
    }


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest_csv)
    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not manifest_path.exists():
        raise FileNotFoundError(f'Manifest not found: {manifest_path}')

    with manifest_path.open('r', encoding='utf-8', newline='') as f:
        manifest_rows = list(csv.DictReader(f))

    out_fields = [
        'run_id',
        'run_finished_at',
        'run_status',
        'machine',
        'operator',
        'model',
        'prompt_version',
        'rows_requested',
        'rows_processed',
        'runtime_sec',
        'output_csv',
        'output_exists',
        'output_rows',
        'nonempty_summary_pct',
        'avg_summary_words',
        'median_summary_words',
        'low_rows',
        'mid_rows',
        'high_rows',
    ]

    with output_path.open('w', encoding='utf-8', newline='') as out_f:
        writer = csv.DictWriter(out_f, fieldnames=out_fields)
        writer.writeheader()

        for run in manifest_rows:
            output_csv_path = Path(run.get('output_csv', ''))
            metrics = summarize_output_csv(output_csv_path)
            row = {
                'run_id': run.get('run_id', ''),
                'run_finished_at': run.get('run_finished_at', ''),
                'run_status': run.get('run_status', ''),
                'machine': run.get('machine', ''),
                'operator': run.get('operator', ''),
                'model': run.get('model', ''),
                'prompt_version': run.get('prompt_version', ''),
                'rows_requested': run.get('rows_requested', ''),
                'rows_processed': run.get('rows_processed', ''),
                'runtime_sec': run.get('runtime_sec', ''),
                'output_csv': run.get('output_csv', ''),
                **metrics,
            }
            writer.writerow(row)

    print(f'Wrote run comparison CSV: {output_path}')
    print(f'Runs analyzed: {len(manifest_rows)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

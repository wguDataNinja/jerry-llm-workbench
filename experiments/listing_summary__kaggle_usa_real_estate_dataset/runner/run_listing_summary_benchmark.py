#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
from pathlib import Path
import time
from typing import Any
import urllib.error
import urllib.request


def get_json(url: str, timeout: int = 20) -> dict[str, Any]:
    req = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        return json.loads(resp.read().decode('utf-8'))


def post_json(url: str, payload: dict[str, Any], timeout: int = 120) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        return json.loads(resp.read().decode('utf-8'))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run listing-summary benchmark with local Ollama.')
    parser.add_argument('--input-csv', required=True)
    parser.add_argument('--prompt-file', required=True)
    parser.add_argument('--output-csv', default='')
    parser.add_argument('--model', default='')
    parser.add_argument('--base-url', default=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'))
    parser.add_argument('--machine', default=os.getenv('BENCH_MACHINE', os.getenv('HOSTNAME', os.getenv('COMPUTERNAME', 'unknown-machine'))))
    parser.add_argument('--operator', default=os.getenv('BENCH_OPERATOR', os.getenv('USER', os.getenv('USERNAME', 'unknown-operator'))))
    parser.add_argument('--manifest-csv', default='experiments/listing_summary__kaggle_usa_real_estate_dataset/results/run_manifest.csv')
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Optional row limit. Omit to run all rows.',
    )
    parser.add_argument('--temperature', type=float, default=0.2)
    return parser.parse_args()


def normalize_value(value: str) -> str:
    text = (value or '').strip()
    if text == '' or text.lower() == 'nan':
        return 'unknown'
    return text


def detect_model(base_url: str) -> str:
    tags = get_json(f"{base_url.rstrip('/')}/api/tags")
    models = [m.get('name', '') for m in tags.get('models', []) if isinstance(m, dict)]
    llama_candidates = [m for m in models if m.startswith('llama3')]
    if llama_candidates:
        return sorted(llama_candidates)[0]
    if models:
        return str(models[0])
    raise RuntimeError('No local Ollama models found. Pull a model first.')


def render_prompt(template: str, row: dict[str, str]) -> str:
    values = {
        'status': normalize_value(row.get('status', '')),
        'price': normalize_value(row.get('price', '')),
        'bed': normalize_value(row.get('bed', '')),
        'bath': normalize_value(row.get('bath', '')),
        'acre_lot': normalize_value(row.get('acre_lot', '')),
        'house_size': normalize_value(row.get('house_size', '')),
        'city': normalize_value(row.get('city', '')),
        'state': normalize_value(row.get('state', '')),
        'zip_code': normalize_value(row.get('zip_code', '')),
        'prev_sold_date': normalize_value(row.get('prev_sold_date', '')),
    }
    return template.format(**values)


def clean_summary_text(text: str) -> str:
    cleaned = text.strip()
    prefixes = (
        'Here is a concise property summary:',
        'Concise property summary:',
        'Property summary:',
    )
    for prefix in prefixes:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix) :].strip()
    return cleaned


def append_run_manifest(
    manifest_path: Path,
    *,
    run_id: str,
    run_started_at: str,
    run_finished_at: str,
    machine: str,
    operator: str,
    model: str,
    prompt_version: str,
    input_csv: Path,
    prompt_file: Path,
    output_csv: Path,
    limit: str,
    run_status: str,
    rows_requested: int,
    rows_processed: int,
    temperature: float,
    base_url: str,
    runtime_sec: float,
    note: str,
) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        'run_id',
        'run_started_at',
        'run_finished_at',
        'machine',
        'operator',
        'model',
        'prompt_version',
        'input_csv',
        'prompt_file',
        'output_csv',
        'limit',
        'run_status',
        'rows_requested',
        'rows_processed',
        'temperature',
        'base_url',
        'runtime_sec',
        'note',
    ]
    row = {
        'run_id': run_id,
        'run_started_at': run_started_at,
        'run_finished_at': run_finished_at,
        'machine': machine,
        'operator': operator,
        'model': model,
        'prompt_version': prompt_version,
        'input_csv': str(input_csv),
        'prompt_file': str(prompt_file),
        'output_csv': str(output_csv),
        'limit': limit,
        'run_status': run_status,
        'rows_requested': rows_requested,
        'rows_processed': rows_processed,
        'temperature': temperature,
        'base_url': base_url,
        'runtime_sec': f'{runtime_sec:.3f}',
        'note': note,
    }
    should_write_header = not manifest_path.exists() or manifest_path.stat().st_size == 0
    with manifest_path.open('a', encoding='utf-8', newline='') as dst:
        writer = csv.DictWriter(dst, fieldnames=fields)
        if should_write_header:
            writer.writeheader()
        writer.writerow(row)


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_csv)
    prompt_path = Path(args.prompt_file)
    manifest_path = Path(args.manifest_csv)

    if not input_path.exists():
        raise FileNotFoundError(f'Input CSV not found: {input_path}')
    if not prompt_path.exists():
        raise FileNotFoundError(f'Prompt file not found: {prompt_path}')
    if args.limit is not None and args.limit <= 0:
        raise ValueError('--limit must be a positive integer when provided.')

    model = args.model.strip() if args.model.strip() else detect_model(args.base_url)
    prompt_template = prompt_path.read_text(encoding='utf-8')

    run_started = dt.datetime.now()
    started_monotonic = time.monotonic()
    timestamp = run_started.strftime('%Y%m%d_%H%M%S')
    default_output = Path(
        f"experiments/listing_summary__kaggle_usa_real_estate_dataset/results/listing_summary_v0__{model.replace(':', '_')}__{timestamp}.csv"
    )
    output_path = Path(args.output_csv) if args.output_csv else default_output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open('r', encoding='utf-8', newline='') as src:
        reader = csv.DictReader(src)
        rows = list(reader)

    if args.limit is not None:
        rows = rows[: args.limit]
    rows_requested = len(rows)

    out_fields = [
        'listing_id',
        'model',
        'prompt_version',
        'price_band',
        'status',
        'price',
        'bed',
        'bath',
        'acre_lot',
        'house_size',
        'city',
        'state',
        'zip_code',
        'prev_sold_date',
        'summary_text',
        'prompt_eval_count',
        'eval_count',
        'total_duration_ns',
    ]

    url = f"{args.base_url.rstrip('/')}/api/generate"

    print(
        f'Run starting | model={model} | machine={args.machine} | '
        f'operator={args.operator} | rows={rows_requested}'
    )

    run_status = 'completed'
    note = ''
    rows_processed = 0
    interrupted = False
    pending_error: Exception | None = None

    try:
        with output_path.open('w', encoding='utf-8', newline='') as dst:
            writer = csv.DictWriter(dst, fieldnames=out_fields)
            writer.writeheader()

            for idx, row in enumerate(rows, start=1):
                prompt = render_prompt(prompt_template, row)
                payload = {
                    'model': model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {'temperature': args.temperature},
                }
                try:
                    data = post_json(url, payload)
                except urllib.error.HTTPError as exc:
                    body = exc.read().decode('utf-8', errors='replace')
                    raise RuntimeError(f'Ollama HTTP {exc.code}: {body}') from exc
                except urllib.error.URLError as exc:
                    reason = getattr(exc, 'reason', exc)
                    raise RuntimeError(f'Could not reach Ollama at {url}: {reason}') from exc

                summary_text = clean_summary_text(str(data.get('response', '')).strip())
                writer.writerow(
                    {
                        'listing_id': row.get('listing_id', f'row-{idx:03d}'),
                        'model': model,
                        'prompt_version': 'v0',
                        'price_band': row.get('price_band', ''),
                        'status': row.get('status', ''),
                        'price': row.get('price', ''),
                        'bed': row.get('bed', ''),
                        'bath': row.get('bath', ''),
                        'acre_lot': row.get('acre_lot', ''),
                        'house_size': row.get('house_size', ''),
                        'city': row.get('city', ''),
                        'state': row.get('state', ''),
                        'zip_code': row.get('zip_code', ''),
                        'prev_sold_date': row.get('prev_sold_date', ''),
                        'summary_text': summary_text,
                        'prompt_eval_count': data.get('prompt_eval_count', ''),
                        'eval_count': data.get('eval_count', ''),
                        'total_duration_ns': data.get('total_duration', ''),
                    }
                )
                rows_processed = idx
                if idx == rows_requested or idx % 10 == 0:
                    print(f'Progress: {idx}/{rows_requested}')
    except KeyboardInterrupt:
        run_status = 'aborted'
        note = 'Interrupted by user'
        interrupted = True
        print('\nRun interrupted by user. Finalizing manifest entry...')
    except Exception as exc:  # noqa: BLE001
        run_status = 'failed'
        note = str(exc)
        pending_error = exc

    run_finished = dt.datetime.now()
    runtime_sec = time.monotonic() - started_monotonic
    run_id = f'{timestamp}__{model.replace(":", "_")}__{args.machine}'
    append_run_manifest(
        manifest_path,
        run_id=run_id,
        run_started_at=run_started.isoformat(timespec='seconds'),
        run_finished_at=run_finished.isoformat(timespec='seconds'),
        machine=args.machine,
        operator=args.operator,
        model=model,
        prompt_version='v0',
        input_csv=input_path,
        prompt_file=prompt_path,
        output_csv=output_path,
        limit='all' if args.limit is None else str(args.limit),
        run_status=run_status,
        rows_requested=rows_requested,
        rows_processed=rows_processed,
        temperature=args.temperature,
        base_url=args.base_url,
        runtime_sec=runtime_sec,
        note=note,
    )

    print(
        f'Run complete | status={run_status} | rows={rows_processed}/{rows_requested} | '
        f'runtime_sec={runtime_sec:.3f}'
    )
    print(f'Output CSV: {output_path}')
    print(f'Manifest: {manifest_path}')

    if interrupted:
        return 130
    if pending_error is not None:
        raise RuntimeError(note) from pending_error
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

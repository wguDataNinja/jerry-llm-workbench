from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

from env_utils import load_dotenv


def bytes_to_gb(size_bytes: int) -> str:
    return f'{size_bytes / (1024 ** 3):.2f} GB'


def main() -> int:
    load_dotenv()
    base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434').rstrip('/')
    url = f'{base_url}/api/tags'

    request = urllib.request.Request(url, method='GET')

    try:
        with urllib.request.urlopen(request, timeout=8) as response:  # noqa: S310
            payload = response.read().decode('utf-8')
    except urllib.error.URLError as exc:
        reason = getattr(exc, 'reason', exc)
        print(f'Could not reach Ollama at {url}: {reason}', file=sys.stderr)
        print('Start Ollama and try again.', file=sys.stderr)
        return 1

    data = json.loads(payload)
    models = data.get('models', [])

    print('== Local Ollama Models ==')
    if not models:
        print('No local models found.')
        print('Try: ollama pull qwen2.5-coder:7b')
        return 0

    for model in sorted(models, key=lambda m: m.get('name', '')):
        name = model.get('name', 'unknown')
        size_bytes = int(model.get('size', 0))
        modified_at = str(model.get('modified_at', 'unknown'))
        modified_short = modified_at.split('T')[0] if 'T' in modified_at else modified_at
        print(f'- {name:30} {bytes_to_gb(size_bytes):>10}  updated {modified_short}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

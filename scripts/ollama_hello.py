from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

from env_utils import load_dotenv

PROMPT = (
    "Say hello to Jerry in 3 short sentences. "
    "Mention your model name and that you are ready to help with coding tasks."
)


def main() -> int:
    load_dotenv()

    base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434').rstrip('/')
    model = os.getenv('OLLAMA_DEFAULT_MODEL', 'qwen2.5-coder:7b')
    url = f'{base_url}/api/generate'

    payload = {
        'model': model,
        'prompt': PROMPT,
        'stream': False,
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310
            raw = response.read().decode('utf-8')
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        print(f'Ollama returned HTTP {exc.code}: {body}', file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        reason = getattr(exc, 'reason', exc)
        print(f'Could not reach Ollama at {url}: {reason}', file=sys.stderr)
        print('Is Ollama running? Start it and try again.', file=sys.stderr)
        return 1

    data = json.loads(raw)
    response_text = str(data.get('response', '')).strip()

    print('== Ollama Hello ==')
    print(f'Model: {model}')
    print('')
    if response_text:
        print(response_text)
        return 0

    print('Model call succeeded, but no response text was returned.')
    print(json.dumps(data, indent=2))
    return 1


if __name__ == '__main__':
    raise SystemExit(main())

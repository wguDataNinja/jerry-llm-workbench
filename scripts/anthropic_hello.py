from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

from env_utils import load_dotenv

PROMPT = (
    'Say hello to Jerry in 3 short sentences. '
    'Mention that you are ready to help with coding tasks and repository setup.'
)


def extract_content_text(data: dict) -> str:
    content = data.get('content', [])
    for item in content:
        if item.get('type') == 'text':
            text = str(item.get('text', '')).strip()
            if text:
                return text
    return ''


def main() -> int:
    load_dotenv()

    api_key = os.getenv('ANTHROPIC_API_KEY', '').strip()
    if not api_key:
        print('ANTHROPIC_API_KEY is missing. Add it to .env first.', file=sys.stderr)
        return 1

    base_url = os.getenv('ANTHROPIC_BASE_URL', 'https://api.anthropic.com').rstrip('/')
    model = os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-latest').strip()
    version = os.getenv('ANTHROPIC_VERSION', '2023-06-01').strip()
    url = f'{base_url}/v1/messages'

    payload = {
        'model': model,
        'max_tokens': 200,
        'messages': [
            {
                'role': 'user',
                'content': PROMPT,
            }
        ],
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'x-api-key': api_key,
            'anthropic-version': version,
            'content-type': 'application/json',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310
            raw = response.read().decode('utf-8')
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        print(f'Anthropic returned HTTP {exc.code}: {body}', file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        reason = getattr(exc, 'reason', exc)
        print(f'Could not reach Anthropic at {url}: {reason}', file=sys.stderr)
        return 1

    data = json.loads(raw)
    text = extract_content_text(data)

    print('== Anthropic Hello ==')
    print(f'Model: {model}')
    print('')
    if text:
        print(text)
        return 0

    print('Request succeeded, but no text content was returned.')
    print(json.dumps(data, indent=2))
    return 1


if __name__ == '__main__':
    raise SystemExit(main())

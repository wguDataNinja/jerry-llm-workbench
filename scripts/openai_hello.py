from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

from env_utils import load_dotenv

PROMPT = (
    'Say hello to Jerry in 3 short sentences. '
    'Mention that you are ready to help with coding, Python, and git workflows.'
)


def extract_output_text(data: dict) -> str:
    output_text = data.get('output_text')
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    for item in data.get('output', []):
        if item.get('type') != 'message':
            continue
        for content in item.get('content', []):
            if content.get('type') in {'output_text', 'text'}:
                text = str(content.get('text', '')).strip()
                if text:
                    return text

    return ''


def main() -> int:
    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    if not api_key:
        print('OPENAI_API_KEY is missing. Add it to .env first.', file=sys.stderr)
        return 1

    base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1').rstrip('/')
    model = os.getenv('OPENAI_MODEL', 'gpt-4.1-mini').strip()
    url = f'{base_url}/responses'

    payload = {
        'model': model,
        'input': PROMPT,
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310
            raw = response.read().decode('utf-8')
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        print(f'OpenAI returned HTTP {exc.code}: {body}', file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        reason = getattr(exc, 'reason', exc)
        print(f'Could not reach OpenAI at {url}: {reason}', file=sys.stderr)
        return 1

    data = json.loads(raw)
    text = extract_output_text(data)

    print('== OpenAI Hello ==')
    print(f'Model: {model}')
    print('')
    if text:
        print(text)
        return 0

    print('Request succeeded, but no output text was returned.')
    print(json.dumps(data, indent=2))
    return 1


if __name__ == '__main__':
    raise SystemExit(main())

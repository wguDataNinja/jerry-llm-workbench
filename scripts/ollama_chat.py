from __future__ import annotations

import json
import os
import sys
from typing import Any
import urllib.error
import urllib.request

from env_utils import load_dotenv

QUIT_COMMANDS = {'quit', 'exit'}


def get_json(url: str, timeout: int = 8) -> dict[str, Any]:
    request = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
        return json.loads(response.read().decode('utf-8'))


def post_json(url: str, payload: dict[str, Any], timeout: int = 90) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
        return json.loads(response.read().decode('utf-8'))


def check_ollama_server(base_url: str) -> tuple[bool, str]:
    url = f'{base_url.rstrip("/")}/api/tags'
    try:
        data = get_json(url)
    except urllib.error.URLError as exc:
        reason = getattr(exc, 'reason', exc)
        return False, f'Could not reach Ollama at {url}: {reason}'
    except Exception as exc:  # noqa: BLE001
        return False, f'Unexpected error contacting Ollama: {exc}'

    model_count = len(data.get('models', []))
    return True, f'Ollama is reachable ({model_count} model(s) found).'


def chat_once(base_url: str, model: str, messages: list[dict[str, str]]) -> dict[str, Any]:
    url = f'{base_url.rstrip("/")}/api/chat'
    payload = {
        'model': model,
        'messages': messages,
        'stream': False,
    }

    return post_json(url, payload)


def extract_token_counts(data: dict[str, Any]) -> tuple[int | None, int | None]:
    prompt_count = data.get('prompt_eval_count')
    response_count = data.get('eval_count')

    prompt_tokens = prompt_count if isinstance(prompt_count, int) else None
    response_tokens = response_count if isinstance(response_count, int) else None
    return prompt_tokens, response_tokens


def main() -> int:
    load_dotenv()

    base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434').rstrip('/')
    model = os.getenv('OLLAMA_DEFAULT_MODEL', 'qwen2.5-coder:7b').strip()

    ok, detail = check_ollama_server(base_url)
    if not ok:
        print(detail, file=sys.stderr)
        print('Start Ollama and try again.', file=sys.stderr)
        return 1

    running_total_tokens = 0
    messages: list[dict[str, str]] = []

    print('== Ollama Terminal Chat ==')
    print(f'Model: {model}')
    print(f'Base URL: {base_url}')
    print('Type your message and press Enter.')
    print("Type 'quit' or 'exit' to end the chat.")
    print('')

    while True:
        try:
            user_input = input('You: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nEnding chat.')
            break

        if not user_input:
            continue

        if user_input.lower() in QUIT_COMMANDS:
            print('Ending chat.')
            break

        messages.append({'role': 'user', 'content': user_input})

        try:
            response_data = chat_once(base_url, model, messages)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode('utf-8', errors='replace')
            print(f'Ollama returned HTTP {exc.code}: {body}', file=sys.stderr)
            print('Chat ended due to request error.', file=sys.stderr)
            return 1
        except urllib.error.URLError as exc:
            reason = getattr(exc, 'reason', exc)
            print(f'Could not reach Ollama at {base_url}/api/chat: {reason}', file=sys.stderr)
            print('Chat ended because Ollama is not reachable.', file=sys.stderr)
            return 1
        except Exception as exc:  # noqa: BLE001
            print(f'Unexpected chat error: {exc}', file=sys.stderr)
            return 1

        assistant_message = response_data.get('message', {})
        assistant_text = str(assistant_message.get('content', '')).strip()
        if not assistant_text:
            assistant_text = '(No response text returned.)'

        print('')
        print(f'Assistant: {assistant_text}')
        print('')

        messages.append({'role': 'assistant', 'content': assistant_text})

        prompt_tokens, response_tokens = extract_token_counts(response_data)
        if prompt_tokens is not None and response_tokens is not None:
            running_total_tokens += prompt_tokens + response_tokens
            print(
                '[Tokens] '
                f'Prompt: {prompt_tokens} | Response: {response_tokens} | '
                f'Session total: {running_total_tokens}'
            )
        else:
            token_summary = 'Token counts are not available from the current response.'
            print(f'[Tokens] {token_summary}')

        print('')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

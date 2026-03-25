from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

from env_utils import load_dotenv


def print_result(label: str, ok: bool, detail: str) -> None:
    status = '[OK]' if ok else '[WARN]'
    print(f'{status} {label}: {detail}')


def first_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ''


def command_status(command: str, args: list[str] | None = None) -> tuple[bool, str]:
    args = args or ['--version']
    executable = shutil.which(command)
    if not executable:
        return False, f'{command} not found in PATH'

    try:
        completed = subprocess.run(
            [command, *args],
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
    except Exception as exc:  # noqa: BLE001
        return False, f'Failed to run {command}: {exc}'

    output = first_line(completed.stdout) or first_line(completed.stderr)
    if completed.returncode != 0:
        note = output or f'version command returned code {completed.returncode}'
        return True, f'found at {executable} (version check issue: {note})'

    return True, output or f'found at {executable}'


def ollama_server_status(base_url: str) -> tuple[bool, str]:
    url = f"{base_url.rstrip('/')}/api/tags"
    request = urllib.request.Request(url, method='GET')

    try:
        with urllib.request.urlopen(request, timeout=6) as response:  # noqa: S310
            payload = response.read().decode('utf-8')
        data = json.loads(payload)
        model_count = len(data.get('models', []))
        return True, f'Ollama API reachable ({model_count} model(s) found)'
    except urllib.error.URLError as exc:
        reason = getattr(exc, 'reason', exc)
        return False, f'Could not reach {url} ({reason})'
    except Exception as exc:  # noqa: BLE001
        return False, f'Unexpected error contacting Ollama API: {exc}'


def main() -> int:
    env_path = load_dotenv()
    ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

    print('== Jerry LLM Workbench: System Check ==')
    print(f'OS: {platform.platform()}')
    print(f'Python: {sys.version.split()[0]} ({sys.executable})')
    print(f'.env loaded: {str(env_path) if env_path else "not found"}')
    print('')

    checks: list[tuple[str, bool, str]] = []

    min_version = (3, 10)
    py_ok = sys.version_info >= min_version
    checks.append(
        (
            'Python version',
            py_ok,
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            + ('' if py_ok else ' (need 3.10+)'),
        )
    )

    in_venv = sys.prefix != getattr(sys, 'base_prefix', sys.prefix)
    checks.append(
        (
            'Virtual environment',
            in_venv,
            'active' if in_venv else 'not active (recommended: use .venv)',
        )
    )

    env_exists = env_path is not None
    checks.append(
        (
            '.env file',
            env_exists,
            'loaded' if env_exists else 'not found (copy .env.example to .env)',
        )
    )

    for command in ('git', 'code', 'ollama'):
        ok, detail = command_status(command)
        checks.append((f'{command} command', ok, detail))

    api_ok, api_detail = ollama_server_status(ollama_base_url)
    checks.append(('Ollama API', api_ok, api_detail))

    warnings = 0
    for label, ok, detail in checks:
        print_result(label, ok, detail)
        if not ok:
            warnings += 1

    print('')
    print(f'Summary: {len(checks) - warnings} passed, {warnings} warning(s).')

    if warnings:
        print('')
        print('Recommended next actions:')
        print('1) Run setup script to create/refresh .venv and .env')
        print('2) Ensure Ollama is installed and running (ollama serve)')
        print('3) Pull a model (example: ollama pull qwen2.5-coder:7b)')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

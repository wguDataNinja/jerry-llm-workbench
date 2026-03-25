from __future__ import annotations

import os
from pathlib import Path


def _candidate_paths(dotenv_path: str | None = None) -> list[Path]:
    if dotenv_path:
        return [Path(dotenv_path)]

    repo_root = Path(__file__).resolve().parents[1]
    return [Path.cwd() / '.env', repo_root / '.env']


def load_dotenv(dotenv_path: str | None = None) -> Path | None:
    """Load key=value pairs from a .env file into os.environ if present."""
    for path in _candidate_paths(dotenv_path):
        if path.exists() and path.is_file():
            _parse_dotenv(path)
            return path
    return None


def _parse_dotenv(path: Path) -> None:
    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()

        if key.startswith('export '):
            key = key[len('export ') :].strip()

        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]

        os.environ.setdefault(key, value)

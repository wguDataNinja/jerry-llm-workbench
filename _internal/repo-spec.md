# Repo Spec (Full Detail)

## 1) Repository Identity
- Canonical repo URL: `https://github.com/wguDataNinja/jerry-llm-workbench`
- Intended default branch: `main`
- Repository role: bootstrap + smoke-test workbench for first-time LLM/agent setup
- Primary onboarding target: Windows 10/11 users (Mac/Linux supported)
- Naming standard in docs/examples: `jerry-llm-workbench`

## 2) Scope And Non-Goals
- In scope:
  - Machine bootstrap for Python + Git + VS Code + Ollama workflows
  - Local LLM smoke tests
  - Optional hosted API smoke tests (OpenAI and Anthropic)
  - Lightweight documentation templates for repeatable setup
- Out of scope:
  - Production deployment
  - Complex package/dependency orchestration
  - Framework-specific app scaffolding
  - Secret management beyond local `.env` for day-1 setup

## 3) Platform And Toolchain Contract
- OS targets:
  - Primary: Windows (PowerShell path)
  - Secondary: macOS/Linux (bash path)
- Python:
  - Required: `3.11+` (scripts are stdlib-only)
  - Minimum tolerated by checks: `3.10+`
- Git:
  - Required for clone/push workflows
- VS Code:
  - Recommended editor for running scripts and using coding agents
- Ollama:
  - Required for local model tests
  - Default endpoint: `http://localhost:11434`

## 4) Repository File Contract
- Root files:
  - `README.md`: top-level source of truth
  - `.gitignore`: prevents local secrets/artifacts from being tracked
  - `.env.example`: template for local configuration
  - `requirements.txt`: intentionally minimal baseline dependency file
  - `setup_windows.ps1`: Windows bootstrap entrypoint
  - `setup_unix.sh`: Unix/macOS bootstrap entrypoint
- `scripts/`:
  - `env_utils.py`: local `.env` loader utility
  - `system_check.py`: host/tooling readiness checks
  - `ollama_model_list.py`: list local Ollama models
  - `ollama_hello.py`: local generation smoke test
  - `ollama_chat.py`: interactive terminal chat for local Ollama models
  - `openai_hello.py`: hosted OpenAI smoke test
  - `anthropic_hello.py`: hosted Anthropic smoke test
- `templates/`:
  - `buddy-system-profile.md`: Buddy system inventory + setup notes template
  - `jerry-system-profile.md`: system inventory + setup notes template
- `_internal/`:
  - `repo-spec.md`: full repository contract
  - `setup-log.md`: append-only setup/troubleshooting log

## 5) Setup Contract
- Windows bootstrap (`setup_windows.ps1`) must:
  - Detect `py` or `python`
  - Create `.venv` if absent
  - Ensure `pip` is available
  - Attempt `pip` upgrade (non-fatal if it fails)
  - Install `requirements.txt`
  - Create `.env` from `.env.example` when missing
- Unix bootstrap (`setup_unix.sh`) must perform equivalent steps for bash users.

## 6) Environment Variable Contract
- Required for local Ollama flow:
  - `OLLAMA_BASE_URL` (default: `http://localhost:11434`)
  - `OLLAMA_DEFAULT_MODEL` (default: `qwen2.5-coder:7b`)
- Optional for OpenAI flow:
  - `OPENAI_API_KEY`
  - `OPENAI_BASE_URL` (default: `https://api.openai.com/v1`)
  - `OPENAI_MODEL` (default: `gpt-4.1-mini`)
- Optional for Anthropic flow:
  - `ANTHROPIC_API_KEY`
  - `ANTHROPIC_BASE_URL` (default: `https://api.anthropic.com`)
  - `ANTHROPIC_MODEL` (default: `claude-3-5-sonnet-latest`)
  - `ANTHROPIC_VERSION` (default: `2023-06-01`)

## 7) Script Behavior Contract
- All scripts:
  - Must run directly via `python scripts/<name>.py`
  - Must print human-readable status
  - Must fail with clear actionable messages
  - Should avoid external dependencies unless justified
- `system_check.py`:
  - Reports Python, venv state, `.env` presence, Git/VS Code/Ollama command availability, and Ollama API reachability
- `ollama_*` scripts:
  - Must fail clearly when Ollama is not reachable
- API smoke tests:
  - Must fail fast when API keys are missing

## 8) Security And Secret Handling Contract
- `.env` is always local-only and must not be committed.
- `.env.example` is the only committed env config file.
- No hard-coded API keys or tokens in repo files.
- Internal notes that may contain sensitive local details stay in `_internal/`.

## 9) Git And Collaboration Contract
- Keep changes small and reviewable.
- Prefer one focused commit per logical change.
- Keep `README.md` current when setup flow changes.
- Avoid large refactors unless explicitly planned.

## 10) Validation Contract
- Minimum pre-push checks:
  - `python3 -m py_compile scripts/*.py`
  - `python3 scripts/system_check.py`
- Optional environment-dependent checks:
  - `python3 scripts/ollama_model_list.py`
  - `python3 scripts/ollama_hello.py`
  - `python3 scripts/openai_hello.py`
  - `python3 scripts/anthropic_hello.py`

## 11) Extension Rules
- New scripts should do one thing and remain beginner-friendly.
- Add new configuration keys to `.env.example` and document them in `README.md`.
- Keep top-level structure stable so coding agents can navigate predictably.

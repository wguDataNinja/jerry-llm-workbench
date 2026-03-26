# Setup Log

Use this log for practical setup notes and troubleshooting details.

## Entry Template
- Date:
- Owner:
- Change:
- Commands run:
- Result:
- Follow-up:

---

## 2026-03-25
- Date: 2026-03-25
- Owner: Jerry (Claude Code)
- Change: First proof-of-life setup on Jerry's Windows machine.
- Commands run:
  - `git clone https://github.com/wguDataNinja/jerry-llm-workbench`
  - `powershell -ExecutionPolicy Bypass -File setup_windows.ps1` (created .venv, installed pip, created .env from .env.example)
  - `.venv/Scripts/python.exe scripts/system_check.py` — 7 passed, 0 warnings
  - `.venv/Scripts/python.exe scripts/ollama_model_list.py` — listed 3 models
  - `.venv/Scripts/python.exe scripts/ollama_hello.py` — response received from llama3:latest
- Result: All three smoke tests passed. System fully operational.
- Follow-up:
  - Create GitHub account and configure push access
  - Run full 50-row benchmark: `python experiments/.../run_listing_summary_benchmark.py`
  - Add hosted API keys when ready

---

## 2026-03-17
- Date: 2026-03-17
- Owner: Buddy
- Change: Bootstrapped this repository for Jerry's Windows onboarding.
- Commands run:
  - Created setup scripts and smoke-test scripts.
  - Added `.env.example`, `.gitignore`, and templates.
- Result: Repo now has a runnable day-1 workflow.
- Follow-up: Jerry should run `setup_windows.ps1` on his Windows PC.

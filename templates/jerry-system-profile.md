# Jerry System Profile

## Machine
- Date: 2026-03-25
- Device name: DESKTOP-NGVG1SS
- OS + version: Windows 11 Pro 10.0.26200
- CPU: AMD Ryzen 7 5800X 8-Core Processor
- GPU: NVIDIA GeForce RTX 4060 Ti
- RAM: 128 GB
- Storage: ~930 GB SSD (C: drive)

## Core Toolchain
- Python version: 3.13.12
- Environment tools: venv
- Git version: 2.53.0.windows.2
- VS Code version: 1.113.0
- Primary coding agent (Codex or Claude Code): Claude Code
- Additional coding tools (Copilot, etc.): none yet
- GitHub username: bearclawbob

## Local Model Setup
- Ollama version: 0.18.2
- Ollama install path: C:\Users\Jerry's 460\AppData\Local\Programs\Ollama\ollama.exe
- Models installed:
  - llama3:latest
  - llama3:70b
  - gpt-oss:20b
- Default model in `.env`: llama3:latest
- Notes on speed/quality:
  - llama3:latest is the active default for smoke tests and benchmark runs
  - llama3:70b and gpt-oss:20b available for higher-quality runs

## Optional Hosted APIs
- OpenAI configured: no
- Anthropic configured: no
- Notes:
  - local Ollama is the primary path; hosted APIs deferred until local workflow is stable

## Workflow Notes
- Preferred terminal: VS Code terminal (Windows native, no WSL)
- Using WSL: no
- Known setup issues:
  - .env default model was qwen2.5-coder:7b (not installed); updated to llama3:latest
- Fixes applied:
  - Changed OLLAMA_DEFAULT_MODEL in .env to llama3:latest to match installed models

## Next Improvements
- 1. Create GitHub account and push first commit
- 2. Run full 50-row benchmark and compare with Buddy's results
- 3. Add hosted API keys when local workflow is stable

# Buddy System Profile

## Machine
- Date: March 18, 2026
- Device name: Buddy’s MacBook Pro
- OS + version: macOS 14.6.1
- CPU: Apple M3 Pro
- GPU: Integrated Apple GPU (M3 Pro)
- RAM: 18 GB unified memory
- Storage: 1TB-class SSD

## Core Toolchain
- Python version: 3.14.2
- Environment tools: venv, pyenv
- Git version: 2.51.1
- VS Code version: 1.111.0
- Primary coding agent (Codex or Claude Code): Codex and Claude Code
- Additional coding tools: GitHub Copilot (secondary)
- GitHub username: wguDataNinja

## Local Model Setup
- Ollama version: 0.17.4
- Ollama install path: /opt/homebrew/bin/ollama
- Models installed:
  - qwen3.5:9b
  - llama3.1
  - codestral
  - mistral:7b-instruct
  - qwen2.5-coder:7b
  - llama3
- Default model in `.env`: qwen3.5:9b
- Notes on speed/quality:
  - qwen3.5:9b is the current primary general-purpose local model
  - published context: 100k+ tokens
  - practical working context on this machine: approximately 40k tokens

## Optional Hosted APIs
- OpenAI configured: yes
- Anthropic configured: yes
- Notes:
  - hosted APIs are available, but local Ollama is a core part of the workflow
  - local-first is preferred for bootstrap and experimentation

## Workflow Notes
- Preferred terminal: VS Code terminal on macOS
- Using WSL: no (native macOS workflow)
- Known setup issues:
  - none recorded here yet
- Fixes applied:
  - none recorded here yet

## Next Improvements
- 1. Keep version fields current after tool upgrades
- 2. Add structured performance notes by model (speed, quality, context behavior)
- 3. Record recurring setup issues and fixes in `_internal/setup-log.md`

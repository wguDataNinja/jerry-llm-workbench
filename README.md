# Jerry LLM Workbench

## Readme Location
https://github.com/wguDataNinja/jerry-llm-workbench

## Purpose
This repo is meant to get Jerry operational quickly in an agent-assisted coding workflow.

Local Ollama setup comes first. Hosted APIs come later.

## Access And Collaboration
- The repo stays public at first.
- Jerry can read and clone it publicly without a GitHub account.
- A GitHub account is required later for pushing changes, collaboration, and private sharing.
- After Jerry has GitHub access and a successful local clone, this repo will be made private for collaboration.

## Manual Steps (Do Yourself First)
Complete these manually before asking an agent to automate setup.

1. Install Python for Windows
- https://www.python.org/downloads/windows/
- Install Python `3.14.3`
- Choose `Download Windows installer (64-bit)`
- Do not choose `32-bit`, `ARM64`, or `embeddable package`
- If offered, enable `Add Python to PATH`

2. Install Git for Windows
- https://git-scm.com/downloads/win

3. Install VS Code
- https://code.visualstudio.com/Download

4. Install Ollama
- https://ollama.com/download

5. Install one coding agent in VS Code
- Codex or Claude Code (pick one primary agent first)

## After Agent Is Installed (What To Tell Codex/Claude Code)
Yes, this is the right move: give the repo link and say "clone this."

Example prompt you can paste:

```text
Clone this repo and help me finish setup:
https://github.com/wguDataNinja/jerry-llm-workbench
```

Then ask the agent to run:
- `setup_windows.ps1`
- local Ollama smoke tests
- first proof-of-life commit

## Agent Choice
Start with one primary coding agent only.
- Option 1: Codex
- Option 2: Claude Code

Both are viable. Day-one rule: use one primary agent and add the second later only if needed.

## What This Repo Includes
- A Windows-first setup script: `setup_windows.ps1`
- A Mac/Linux setup script for compatibility: `setup_unix.sh`
- Smoke-test scripts for local Ollama and optional hosted APIs
- A starter `.env.example` and sensible `.gitignore`
- Template docs for system profiles and setup logging

## Windows Quickstart
Local Ollama setup comes first because it avoids API keys, billing setup, and external dependencies during bring-up, and keeps local data private on Jerry's machine.

### 1) Verify Installs

```powershell
py -3 --version
git --version
ollama --version
```

Note: on Windows, Python may appear as `py` instead of `python`.

### 2) Clone And Enter Repo
Jerry can clone this repo before creating a GitHub account.

Use Codex or Claude Code to help with this step if needed.

```powershell
git clone https://github.com/wguDataNinja/jerry-llm-workbench.git
cd jerry-llm-workbench
```

### 3) Run Bootstrap Script

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup_windows.ps1
```

### 4) Pull A First Local Model

```powershell
ollama pull qwen2.5-coder:7b
```

### 5) Run Smoke Tests

```powershell
.\.venv\Scripts\python.exe scripts\system_check.py
.\.venv\Scripts\python.exe scripts\ollama_model_list.py
.\.venv\Scripts\python.exe scripts\ollama_hello.py
```

### 6) Start Terminal Chat (Optional)

```powershell
.\.venv\Scripts\python.exe scripts\ollama_chat.py
```

## First Success
Success means all three are true:
- `scripts/system_check.py` runs
- `scripts/ollama_model_list.py` runs
- `scripts/ollama_hello.py` returns a model response

Good additional signal:
- Jerry can also chat successfully using either the Ollama app or `scripts/ollama_chat.py`

## Fill Out System Profile
- Fill out Jerry's profile: `templates/jerry-system-profile.md`
- Use Buddy's profile as reference: `templates/buddy-system-profile.md`
- Record setup issues, fixes, and notes in `_internal/setup-log.md`

## First Proof-Of-Life Commit
After first success and profile updates:

```powershell
git add templates/jerry-system-profile.md _internal/setup-log.md
git commit -m "chore: first proof of life on Jerry machine"
```

For now, do not push yet.

This local commit proves:
- the repo is cloned
- Git is working
- setup reached first success
- Jerry can begin collaborating once push access is enabled

## Two Ways To Chat With Ollama
- Ollama desktop app GUI: built-in chat interface on Windows and macOS
- Terminal script: `scripts/ollama_chat.py` for quick experimentation in the terminal

## Optional Hosted API Tests
Hosted APIs are secondary to the local Ollama path.

1. Add keys to `.env`:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`

2. Run:

```powershell
.\.venv\Scripts\python.exe scripts\openai_hello.py
.\.venv\Scripts\python.exe scripts\anthropic_hello.py
```

## WSL Guidance
- Start on native Windows first.
- Use WSL only if native Windows causes repeated problems with terminal behavior, Python tooling, or agent workflows.
- If Jerry chooses Codex on Windows, recommend WSL more strongly because Codex IDE support on Windows is documented as experimental and OpenAI recommends a WSL workspace.

References:
- https://developers.openai.com/codex/ide
- https://developers.openai.com/codex/windows
- https://code.visualstudio.com/docs/remote/wsl
- https://learn.microsoft.com/en-us/windows/wsl/

## Repo Layout

```text
jerry-llm-workbench/
├─ README.md
├─ .gitignore
├─ .env.example
├─ requirements.txt
├─ setup_windows.ps1
├─ setup_unix.sh
├─ scripts/
│  ├─ env_utils.py
│  ├─ system_check.py
│  ├─ ollama_model_list.py
│  ├─ ollama_hello.py
│  ├─ ollama_chat.py
│  ├─ openai_hello.py
│  └─ anthropic_hello.py
├─ templates/
│  ├─ buddy-system-profile.md
│  └─ jerry-system-profile.md
└─ _internal/
   ├─ repo-spec.md
   └─ setup-log.md
```

## Repo Spec
- Full spec lives in `_internal/repo-spec.md`
- It defines the working contract for the repo
- It keeps this README focused on setup, gives coding agents a stable reference, and reduces downstream friction

## Script Reference
- `scripts/system_check.py`: checks OS, Python, venv, Git, and Ollama readiness
- `scripts/ollama_model_list.py`: lists local Ollama models
- `scripts/ollama_hello.py`: sends a simple prompt to the default local model
- `scripts/ollama_chat.py`: starts interactive terminal chat with in-memory session history
- `scripts/openai_hello.py`: optional OpenAI API smoke test
- `scripts/anthropic_hello.py`: optional Anthropic API smoke test

## Security Rules
- Never commit `.env`
- Keep real keys only in local `.env`
- Commit `.env.example` only
- Keep local and private notes in `_internal/`

## First-Day Checklist
- [ ] Install Python 3.14.3 (64-bit), Git, VS Code, Ollama
- [ ] Install one coding agent (Codex or Claude Code)
- [ ] Clone this repo
- [ ] Run `setup_windows.ps1`
- [ ] Pull and test one local model
- [ ] Run first local smoke tests
- [ ] Fill out `templates/jerry-system-profile.md`
- [ ] Record setup notes in `_internal/setup-log.md`
- [ ] Make first proof-of-life commit
- [ ] Create GitHub account when ready to push and collaborate

## What Happens Next
- Finish GitHub account setup if not already done
- Push Jerry's first commit and start collaboration
- Make the repo private and share access properly
- Add hosted API keys later only when local workflow is stable

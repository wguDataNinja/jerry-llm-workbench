# AGENTS.md

This file defines baseline rules for coding agents working in this repository.

## Scope And Authorization
- Agents must stay inside this repository unless the user gives explicit authorization for external scope.
- Agents must not access or modify unrelated local folders, repos, services, or infrastructure without explicit approval.
- Sensitive data remains out of this repo. Only masked or anonymized data may be used in-repo.

## Git Hygiene Requirements
- Use small, scoped changes tied to one purpose.
- Write clear commit messages that explain intent.
- Do not use destructive Git operations (`reset --hard`, force push, history rewrite) unless explicitly authorized.
- Do not revert unrelated local changes made by the user or other agents.

## Development Logging
- Every work session should be logged in `_internal/dev_log.md`.
- Log entries should be added in chronological order.
- Each entry must include:
  - Date
  - Machine
  - User
  - Agent
  - Summary of changes
  - Validation performed
  - Risks or follow-ups

## Minimum Validation Standard
- Run the smallest useful check for the changes made.
- If checks are skipped or blocked, record why in the dev log.

## Handoff Standard
- At task completion, record what changed, what was validated, and what remains.

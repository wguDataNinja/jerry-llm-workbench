# Development Log

Use this log for agent-assisted coding sessions.

## Entry Template

### YYYY-MM-DD HH:MM (Local)
- Machine: <example: Buddy's MacBook>
- User: <name>
- Agent: <example: Codex>
- Scope: <what this session was intended to do>
- Changes Made:
  - <file/path + short description>
- Validation:
  - <commands/checks run>
- Risks / Follow-Ups:
  - <open items>
- Sign-off:
  - User: <name>
  - Agent: <agent name>

---

## Session Log

### 2026-03-25 (Local)
- Machine: DESKTOP-NGVG1SS (Jerry's machine)
- User: Jerry
- Agent: Claude Code
- Scope: First proof-of-life setup — clone, bootstrap, smoke tests.
- Changes Made:
  - .env: Changed OLLAMA_DEFAULT_MODEL from qwen2.5-coder:7b to llama3:latest (model not installed)
  - templates/jerry-system-profile.md: Filled out Jerry's machine and toolchain profile
  - _internal/setup-log.md: Added 2026-03-25 setup entry
  - _internal/dev_log.md: Added this session entry
- Validation:
  - scripts/system_check.py: 7 passed, 0 warnings
  - scripts/ollama_model_list.py: 3 models listed (llama3:latest, llama3:70b, gpt-oss:20b)
  - scripts/ollama_hello.py: successful response from llama3:latest
- Risks / Follow-Ups:
  - GitHub account needed before pushing
  - Benchmark run ready: llama3:latest installed and tested
- Sign-off:
  - User: Jerry
  - Agent: Claude Code



### 2026-03-25 17:30 (Local)
- Machine: Buddy's MacBook
- User: Buddy
- Agent: Codex
- Scope: Add agent operating policy and dev-log standards.
- Changes Made:
  - README.md: Added Agent Operating Rules and references to AGENTS.md and dev log.
  - AGENTS.md: Added baseline operating policy for coding agents.
  - _internal/dev_log.md: Added this development log template.
- Validation:
  - Verified file updates and structure by reading files.
- Risks / Follow-Ups:
  - Expand AGENTS.md if branch strategy or CI policy changes.
- Sign-off:
  - User: Buddy
  - Agent: Codex

### 2026-03-25 17:23 (Local)
- Machine: Buddy's MacBook
- User: Buddy
- Agent: Codex
- Scope: Set up Kaggle benchmark workspace and extraction scaffold.
- Changes Made:
  - README.md: Added/updated agent rules and aligned benchmark slug to Kaggle dataset.
  - .gitignore: Ignore raw benchmark data and generated results by default.
  - experiments/listing_summary__kaggle_usa_real_estate_dataset/README.md: Added clean download and sample plan.
  - experiments/listing_summary__kaggle_usa_real_estate_dataset/runner/extract_location_sample.py: Added location-based sample extractor.
  - Added .gitkeep placeholders for raw, samples, and results directories.
- Validation:
  - Verified file content and paths.
  - Verified Kaggle auth/CLI status (not configured on this machine).
- Risks / Follow-Ups:
  - Need Kaggle API credentials to perform download.
  - After download, inspect schema and choose location field/value for sample extraction.
- Sign-off:
  - User: Buddy
  - Agent: Codex

### 2026-03-25 17:28 (Local)
- Machine: Buddy's MacBook
- User: Buddy
- Agent: Codex
- Scope: Local raw dataset ingest and initial location-based sample extraction.
- Changes Made:
  - Copied raw CSV to experiments/listing_summary__kaggle_usa_real_estate_dataset/data/raw/realtor-data.zip.csv.
  - Generated sample: experiments/listing_summary__kaggle_usa_real_estate_dataset/data/samples/st_augustine__sample.csv (50 rows).
  - Generated location profile: experiments/listing_summary__kaggle_usa_real_estate_dataset/data/samples/location_profile_top_city_state.csv.
- Validation:
  - Confirmed dataset schema and row count (2,226,382 rows).
  - Ran extractor script and confirmed sample row count.
- Risks / Follow-Ups:
  - Final publish sample location remains TBD by user preference.
  - If masking rules tighten, apply masking transform before commit.
- Sign-off:
  - User: Buddy
  - Agent: Codex

### 2026-03-25 17:36 (Local)
- Machine: Buddy's MacBook
- User: Buddy
- Agent: Codex
- Scope: Build sold-only ZIP 32092 sample with price buckets and min/max coverage.
- Changes Made:
  - experiments/listing_summary__kaggle_usa_real_estate_dataset/data/samples/st_augustine_32092_sold__price_bands_sample.csv: Created 50-row benchmark sample.
  - experiments/listing_summary__kaggle_usa_real_estate_dataset/data/samples/st_augustine_32092_sold__price_bands_sample.meta.txt: Added filter and band metadata.
- Validation:
  - Verified sample filters: status=sold only, zip_code=32092 only.
  - Verified min and max prices in full match set are included in sample.
  - Verified near-even band distribution across quartile buckets.
- Risks / Follow-Ups:
  - If model robustness testing needs outlier emphasis, increase high-band share.
- Sign-off:
  - User: Buddy
  - Agent: Codex

### 2026-03-25 17:45 (Local)
- Machine: Buddy's MacBook
- User: Buddy
- Agent: Codex
- Scope: Generate sold-only ZIP 32092 sample with low/mid/high price bands.
- Changes Made:
  - Created experiments/listing_summary__kaggle_usa_real_estate_dataset/data/samples/st_augustine_32092_sold__low_mid_high_sample.csv
  - Created experiments/listing_summary__kaggle_usa_real_estate_dataset/data/samples/st_augustine_32092_sold__low_mid_high_sample.meta.txt
- Validation:
  - Confirmed 50 rows, all status=sold, all zip_code=32092.
  - Confirmed price_band column present with distribution low=17, mid=16, high=17.
  - Confirmed sample includes min/max prices from the filtered pool.
- Risks / Follow-Ups:
  - If strict reproducibility is needed, pin this file as canonical sample in experiment README.
- Sign-off:
  - User: Buddy
  - Agent: Codex

### 2026-03-25 17:51 (Local)
- Machine: Buddy's MacBook
- User: Buddy
- Agent: Codex
- Scope: Add v0 listing-summary prompt and runnable Ollama benchmark pipeline.
- Changes Made:
  - Added prompt template: experiments/listing_summary__kaggle_usa_real_estate_dataset/prompts/listing_summary_v0.txt
  - Added input-prep runner: experiments/listing_summary__kaggle_usa_real_estate_dataset/runner/prepare_experiment_input.py
  - Added benchmark runner with --limit support: experiments/listing_summary__kaggle_usa_real_estate_dataset/runner/run_listing_summary_benchmark.py
  - Created benchmark input CSV: experiments/listing_summary__kaggle_usa_real_estate_dataset/data/samples/st_augustine_32092_sold__benchmark_input_v0.csv
  - Ran one-row llama3 test output: experiments/listing_summary__kaggle_usa_real_estate_dataset/results/listing_summary_v0__llama3_latest__single_test.csv
  - Updated experiment README with run commands for smoke test and full run.
- Validation:
  - py_compile passed for both new runner scripts.
  - Single-row run succeeded with model llama3:latest.
- Risks / Follow-Ups:
  - Full 50-row run was not executed per request; use --limit -1 to run full sample.
- Sign-off:
  - User: Buddy
  - Agent: Codex

### 2026-03-25 18:07 (Local)
- Machine: Buddy's MacBook
- User: Buddy
- Agent: Codex
- Scope: Re-run and validate --limit 1 smoke test for listing-summary v0 runner.
- Changes Made:
  - Wrote fresh test output: experiments/listing_summary__kaggle_usa_real_estate_dataset/results/listing_summary_v0__llama3_latest__single_test_latest.csv
- Validation:
  - Confirmed 1 output row and valid summary text.
  - Confirmed filters/fields align with benchmark input row.
- Risks / Follow-Ups:
  - None blocking; full --limit -1 run is ready.
- Sign-off:
  - User: Buddy
  - Agent: Codex

### 2026-03-25 18:30 (Local)
- Machine: Buddy's MacBook
- User: Buddy
- Agent: Codex
- Scope: Add run-manifest logging for cross-machine benchmark tracking.
- Changes Made:
  - Updated runner to append run metadata to results/run_manifest.csv.
  - Added machine/operator CLI args and manifest path arg.
  - Updated experiment README with manifest and Buddy/Jerry command pattern.
  - Updated .gitignore to allow committing run_manifest.csv while ignoring per-run results.
- Validation:
  - Smoke run succeeded and appended manifest row.
- Risks / Follow-Ups:
  - None blocking.
- Sign-off:
  - User: Buddy
  - Agent: Codex

### 2026-03-25 18:32 (Local)
- Machine: Buddy's MacBook
- User: Buddy
- Agent: Codex
- Scope: Clean previous run artifacts and improve runner/manifest behavior for cross-machine runs.
- Changes Made:
  - Cleared prior files in experiments/listing_summary__kaggle_usa_real_estate_dataset/results/ (kept .gitkeep).
  - Updated runner terminal output to concise run start/progress/final stats format.
  - Updated manifest schema to include run_status, rows_requested, and note.
  - Rebuilt fresh smoke artifacts after cleanup.
- Validation:
  - Smoke run completed and wrote fresh output + manifest entry.
  - Manifest now records completed status and runtime.
- Risks / Follow-Ups:
  - None blocking; ready for Buddy full run and Jerry full run.
- Sign-off:
  - User: Buddy
  - Agent: Codex

### 2026-03-25 18:39 (Local)
- Machine: Buddy's MacBook
- User: Buddy
- Agent: Codex
- Scope: Add early experiment coordination section and create no-gold run comparison script.
- Changes Made:
  - README.md: Added early "Current Experiment (Active)" section with Buddy/Jerry flow and commands.
  - experiments/.../README.md: Added compare-run documentation and command.
  - experiments/.../runner/compare_run_outputs.py: Added manifest-driven run comparison script.
- Validation:
  - compare_run_outputs.py compiles and runs.
  - run_comparison.csv generated from current manifest.
- Risks / Follow-Ups:
  - Comparison is descriptive only (no gold labels yet).
- Sign-off:
  - User: Buddy
  - Agent: Codex

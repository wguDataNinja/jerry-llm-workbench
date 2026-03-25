# USA Real Estate Dataset

This benchmark uses a sample derived from the **USA Real Estate Dataset**.

## Experiment in one paragraph
This experiment tests local `llama3` listing summarization quality on a 50-row St. Augustine sold-listing sample (`ZIP 32092`) with `low/mid/high` price bands. The goal is not perfect scoring yet; it is to quickly surface obvious model errors, awkward phrasing, and factual mistakes before expanding to more models and larger samples.

## Current run and review focus
- Run tracking file: `results/run_manifest.csv`
- Completed Buddy full run ID: `20260325_184959__llama3_latest__Buddy-MacBook`
- Buddy shared output CSV: `results/shared/buddy_llama3_v0_full50.csv`
- Buddy LLM-as-judge review: `results/shared/reviews/llama3_buddy_full50_llm_judge_v1.md`
- Next step: Jerry runs the same benchmark input with any installed local model and machine tag.

When reviewing outputs, flag anything silly or wrong:
- invented facts not in row fields
- wrong location, status, or price
- contradictory statements (for example sold + active phrasing)
- repetitive or boilerplate language
- overconfident tone when key fields are missing

## Origin

Source:
- Kaggle
- Dataset: **USA Real Estate Dataset**
- Author: **Ahmed Shahriar Sakib**
- Link: https://www.kaggle.com/datasets/ahmedshahriarsakib/usa-real-estate-dataset

## Source description

The source dataset is described as:

- U.S. real estate listings
- broken out by **state** and **ZIP code**
- distributed as a single CSV file
- approximately **2.2M+ rows**

The source file is:

- `realtor-data.csv`

## Source fields

The source dataset includes these columns:

- `brokered by`
- `status`
- `price`
- `bed`
- `bath`
- `acre_lot`
- `street`
- `city`
- `state`
- `zip_code`
- `house_size`
- `prev_sold_date`

Notes from the source description:

- `brokered by` is categorically encoded
- `street` is categorically encoded
- `acre_lot` represents total land area in acres
- `house_size` represents living space / building area in square feet

## Temporal and geographic coverage

- Temporal coverage: **2022-04-01 to 2022-05-25**
- Geographic coverage: **United States**

## Usage in this repo

The full dataset is **not** stored or shared in this repository.

This repo uses a **sample derived from the source dataset** for benchmark work.

Planned use:
- real-estate listing summarization
- initial benchmark runs with local Ollama models
- first benchmark path focused on a small sample rather than the full corpus

## Sample used in this repo

A local sample is used for experimentation and benchmarking.

Current benchmark sample:
- source dataset: USA Real Estate Dataset
- sample scope: `city in {Saint Augustine, St. Augustine, St Augustine}`, `state=Florida`, `zip_code=32092`, `status=sold`
- sample size: `50` rows
- market focus: sold listings in ZIP `32092`
- field subset for benchmark input: `status, price, bed, bath, acre_lot, city, state, zip_code, house_size, prev_sold_date, price_band`
- added benchmark feature: `price_band` (`low`, `mid`, `high`)

Sample files:
- `data/samples/st_augustine_32092_sold__low_mid_high_sample.csv`
- `data/samples/st_augustine_32092_sold__benchmark_input_v0.csv`

## Prompt and runner (v0)

Prompt:
- `prompts/listing_summary_v0.txt`

Runner scripts:
- `runner/prepare_experiment_input.py`
- `runner/run_listing_summary_benchmark.py`
- `runner/compare_run_outputs.py`

### Build benchmark input CSV

```bash
python3 experiments/listing_summary__kaggle_usa_real_estate_dataset/runner/prepare_experiment_input.py \
  --input-csv experiments/listing_summary__kaggle_usa_real_estate_dataset/data/samples/st_augustine_32092_sold__low_mid_high_sample.csv \
  --output-csv experiments/listing_summary__kaggle_usa_real_estate_dataset/data/samples/st_augustine_32092_sold__benchmark_input_v0.csv
```

### Single-row smoke test

```bash
python3 experiments/listing_summary__kaggle_usa_real_estate_dataset/runner/run_listing_summary_benchmark.py \
  --input-csv experiments/listing_summary__kaggle_usa_real_estate_dataset/data/samples/st_augustine_32092_sold__benchmark_input_v0.csv \
  --prompt-file experiments/listing_summary__kaggle_usa_real_estate_dataset/prompts/listing_summary_v0.txt \
  --model llama3:latest \
  --limit 1
```

### Full 50-row run

Omitting `--limit` means run all rows from the input CSV.

```bash
python3 experiments/listing_summary__kaggle_usa_real_estate_dataset/runner/run_listing_summary_benchmark.py \
  --input-csv experiments/listing_summary__kaggle_usa_real_estate_dataset/data/samples/st_augustine_32092_sold__benchmark_input_v0.csv \
  --prompt-file experiments/listing_summary__kaggle_usa_real_estate_dataset/prompts/listing_summary_v0.txt \
  --machine "Buddy-MacBook" \
  --operator "Buddy" \
  --model llama3:latest \
  --output-csv experiments/listing_summary__kaggle_usa_real_estate_dataset/results/shared/buddy_llama3_v0_full50.csv
```

### Run other installed models

```bash
python3 experiments/listing_summary__kaggle_usa_real_estate_dataset/runner/run_listing_summary_benchmark.py \
  --input-csv experiments/listing_summary__kaggle_usa_real_estate_dataset/data/samples/st_augustine_32092_sold__benchmark_input_v0.csv \
  --prompt-file experiments/listing_summary__kaggle_usa_real_estate_dataset/prompts/listing_summary_v0.txt \
  --machine "Jerry-Machine" \
  --operator "Jerry" \
  --model <model_name> \
  --output-csv experiments/listing_summary__kaggle_usa_real_estate_dataset/results/shared/jerry_<model_slug>_v0_full50.csv
```

## Run manifest

Each completed run appends one row to:
- `results/run_manifest.csv`

Repo policy:
- `results/run_manifest.csv` can be committed for run traceability.
- Shareable benchmark result CSVs should go in `results/shared/` and can be committed.
- Ad-hoc/scratch result CSVs in `results/` (outside `shared/`) stay local by default.

Captured metadata:
- run id
- run start/end time
- machine
- operator
- model
- prompt version
- input CSV / prompt file / output CSV
- limit (`all` or numeric)
- rows processed
- temperature
- Ollama base URL
- runtime seconds

## Cross-run comparison (no gold labels yet)

There is no gold reference dataset yet. For now, we compare runs descriptively across:
- model
- machine/operator
- run status and runtime
- output row counts and summary-length behavior
- low/mid/high band coverage in outputs

Build comparison CSV from the manifest:

```bash
python3 experiments/listing_summary__kaggle_usa_real_estate_dataset/runner/compare_run_outputs.py
```

Output:
- `results/run_comparison.csv`

## LLM-as-judge grading artifacts

Store human/LLM grading notes in:
- `results/shared/reviews/`

Current artifact:
- `results/shared/reviews/llama3_buddy_full50_llm_judge_v1.md`

After Jerry runs, add a parallel review file (same rubric structure) so model and machine outputs can be compared directly.

## Repo handling policy

To keep the repo lightweight and easy to navigate:

- the full upstream dataset is not committed to the repo
- only small benchmark-ready sample data may be stored locally in the experiment area
- any derived sample should preserve traceability back to the original Kaggle source

## License and usage note

The source dataset page states that the data is intended for **educational purposes only** and that rights remain with the respective owners.

Anyone using this benchmark setup should review the source dataset page directly before downloading or reusing the data.

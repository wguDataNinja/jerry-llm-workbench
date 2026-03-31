# LLM-as-Judge Review: Jerry gpt-oss:20b v0 Full 50 — Run 2 (Updated Model)

- Run output reviewed: `results/shared/jerry_gpt-oss_20b_v0_full50_run2.csv`
- Run ID: `20260330_201755__gpt-oss_20b__Jerry-Machine`
- Machine: Jerry-Machine (DESKTOP-NGVG1SS, dual RTX 4060 Ti)
- Model: gpt-oss:20b (updated version, 2026-03-30)
- Evaluator mode: LLM-as-judge
- Reviewer scope: qualitative rubric + comparison against prior run
- Overall grade: **C (6.3/10)**

## Summary judgment
The updated gpt-oss:20b is a small regression from the previous run (C+, 6.6/10). Neutrality improved slightly — fewer invented mid-band qualifiers. However, missing-field handling got worse: the model now explicitly announces missing data in several rows ("No additional details on bedrooms, bathrooms, or interior square footage are available"), which is a direct and more severe violation of the omission rule than the previous "unspecified lot size" pattern. Two high-band rows also reverted to comma-separated field lists instead of prose.

## Rubric

| Category | Weight | Grade | Notes |
|---|---:|---:|---|
| Length / format compliance | 20% | B | Mostly 2-3 sentences under 90 words. Two format outliers (rows 046, 047) output comma-separated lists instead of prose. |
| Inclusion of available facts | 30% | B+ | Price, beds/baths, sqft, lot, location consistently included when available. Good factual coverage. |
| Omission of missing facts | 15% | D- | Worse than prior run. Now explicitly announces missing fields in multiple rows rather than silently omitting. |
| Neutrality | 20% | C+ | Slight improvement — fewer "spacious interior" / "desirable" qualifiers in mid-band rows. Still has "desirable area" in rows 033, 044, 045. |
| No invention / no unsupported claims | 15% | C | New invented claims in rows 001 and 004. Fewer invented qualifiers in mid-band than prior run. |

## Comparison to Prior gpt-oss:20b Run

| Category | Run 1 (prev) | Run 2 (this) | Change |
|---|---|---|---|
| Length / format | B+ | B | Slight regression — 2 comma-list outliers |
| Inclusion of facts | A- | B+ | Slight regression |
| Omission of missing facts | D | D- | Regression — more explicit missing-field announcements |
| Neutrality | C | C+ | Improvement |
| No invention | C- | C | Slight improvement |
| **Overall** | **C+ (6.6)** | **C (6.3)** | **Small regression** |

## What improved
- Fewer invented qualifiers in mid-band rows overall.
- Row 019 is now proper prose (was a raw comma-separated field list in run 1).
- High-band rows 034–036, 043, 048–050 are clean and factual.
- "Spacious interior," "desirable neighborhood," "ample outdoor area" removed from most rows where they appeared in run 1.

## What got worse

### 1) Explicitly announces missing fields — new and worse violation
The prior run said "unspecified lot size." This run goes further:
- `32092-sold-003`: "No additional details on bedrooms, bathrooms, or interior square footage are available."
- `32092-sold-004`: "No additional details on bedrooms, bathrooms, or interior square footage are available."
- `32092-sold-015`: "No lot size information is available."
- `32092-sold-038`: "No lot size information is available."
- `32092-sold-040`: "No lot size is listed."

The prompt states: *if a value is missing, do not mention it.* These outputs not only mention it but dedicate a full sentence to calling it out. This is a more severe form of the same failure pattern.

### 2) New invented claims
- `32092-sold-001`: "The lot offers ample space for outdoor activities." — invented; no activity information in the data.
- `32092-sold-004`: Same phrase — "The lot offers ample space for outdoor activities."
- `32092-sold-038`: "it provides ample room for families" — invented; family suitability not in the data.

### 3) Format outliers in high band
- `32092-sold-046`: `$665,000.00, 5 beds, 4 baths, 3,279 sq ft, located in Saint Augustine, FL 32092.` — comma-separated list, not prose.
- `32092-sold-047`: `$675,000.00, 4 beds, 3 baths, 2,844 sq ft, located in Saint Augustine, FL 32092.` — same pattern.

These two rows appear to be a generation glitch on high-price entries with no lot size. Not present in run 1.

### 4) "Unspecified lot size" pattern persists
Rows 006, 008, 010, 017, 020, 024, 025, 026, 028, 029, 030, 032, 039, 041, 042 still use "unspecified lot size" or similar phrasing. This core failure from run 1 was not fixed.

## Specific examples

### Stronger outputs
- `32092-sold-013`: Clean. Price, beds, baths, sqft, lot. Nothing added.
- `32092-sold-036`: Clean two-sentence factual output.
- `32092-sold-048`: Clean. All available facts, no filler.
- `32092-sold-050`: Clean. Price, beds, baths, sqft, location. Nothing invented.

### Problematic outputs
- `32092-sold-003`: Announces all missing fields in a dedicated sentence.
- `32092-sold-001`, `004`: Invents "ample space for outdoor activities."
- `32092-sold-038`: Invents "ample room for families" + announces missing lot size.
- `32092-sold-046`, `047`: Comma-separated list format instead of prose.

## Bottom line
- Instruction adherence: `6.5/10`
- Factual discipline: `7/10`
- Neutrality: `6.5/10`
- Overall: `6.3/10`

The model update did not address the primary failure (missing field omission) and introduced a more explicit form of the same violation. Neutrality improved marginally. The recommended prompt fix remains the same and is now more urgent:

> *"If a value is missing, omit it entirely from the summary. Do not describe it as unknown, unspecified, unavailable, or unlisted. Do not include a sentence noting its absence."*

With that single prompt addition, gpt-oss:20b would likely reach B range on the next run.

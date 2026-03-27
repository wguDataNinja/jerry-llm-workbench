# LLM-as-Judge Review: Jerry llama3:latest v0 Full 50

- Run output reviewed: `results/shared/jerry_llama3_latest_v0_full50.csv`
- Machine: Jerry-Machine (DESKTOP-NGVG1SS, dual RTX 4060 Ti)
- Evaluator mode: LLM-as-judge
- Reviewer scope: qualitative rubric + targeted failure analysis
- Overall grade: **D+**

## Summary judgment
llama3:latest (8b) on Jerry's machine matches Buddy's run almost exactly in failure mode and severity. Every single output opens with "This charming" and the model never escapes marketing-copy mode. Neutrality is the dominant failure. Factual coverage is adequate but the volume of invented qualifiers and sales language drowns out the useful content.

## Rubric

| Category | Weight | Grade | Notes |
|---|---:|---:|---|
| Length / format compliance | 20% | B | Mostly 2-3 sentences. One row leaked meta-text prefix. Generally under 90 words. |
| Inclusion of available facts | 30% | B- | Core facts usually included. Lot size occasionally skipped when present. |
| Omission of missing facts | 15% | C+ | Does not mention missing beds/baths. Does sometimes use prev_sold_date as sale date. |
| Neutrality | 20% | F | Every row uses promotional language. "Charming" appears 43 of 50 rows. |
| No invention / no unsupported claims | 15% | D- | Extensive invented lifestyle claims. Meta-text leakage in one row. |

## What it did reasonably well
- Does not mention missing beds/baths/sqft.
- Includes price and location consistently.
- Outputs are readable and consistent in structure.
- Length is usually appropriate.

## Main problems

### 1) "Charming" on 43 of 50 rows
The model opens every output with "This charming" (rows 001–043, 045, etc.) or "This stunning" (rows 044, 046, 049, 050 — escalating for high price band). These are not neutral descriptors. The word "charming" appears in 43 out of 50 outputs. This is the defining failure of this run.

### 2) Pervasive sales language
Almost no row is free of promotional adjectives or editorial framing. Examples across the run:
- "great value" — rows 005, 006, 009, 010, 011, 012, 013, 014, 021, 022, 023, 024, 027, 029, 032, 033, 034
- "excellent opportunity" — rows 009, 023, 035
- "ideal place to call home" — rows 020, 026, 049
- "cozy retreat" / "comfortable retreat" — rows 007, 008, 016
- "comfortable living experience" — row 037
- "tranquil retreat" — row 050
- "perfect blend of comfort and convenience" — row 025
- "ideal blend of comfort and value" — row 025

None of these appear in the input data.

### 3) Invented features
Many rows add unsupported physical or lifestyle claims:
- `32092-sold-008`: "plenty of natural light"
- `32092-sold-015`: "easy access to all that Saint Augustine has to offer"
- `32092-sold-016`, `041`: "close to all the city's amenities"
- `32092-sold-030`: "plenty of natural light," "short drive from local attractions"
- `32092-sold-042`: "easy access to local amenities"
- `32092-sold-050`: "perfect for those seeking a tranquil retreat with easy access to local amenities"

### 4) Meta-text leakage
- `32092-sold-011`: Output begins "Here is the concise property summary:" followed by a newline and the actual text. The prompt instruction leaked into the output.

### 5) prev_sold_date treated as sale date
Several rows surface prev_sold_date as a transaction date:
- `32092-sold-018`: "it was sold on October 29, 2021"
- `32092-sold-036`: "it was sold on October 29, 2021"
- `32092-sold-040`: "this property sold on February 18, 2022"
- `32092-sold-043`: "Sold for $584,900 on March 31, 2022"

## Specific examples

### Closer to acceptable
- `32092-sold-019`: Includes core facts, promotional qualifier is mild ("cozy retreat").
- `32092-sold-041`: Short and mostly factual, though still "charming."

### Clearly bad outputs
- `32092-sold-008`: "plenty of natural light" — invented.
- `32092-sold-011`: Meta-text leaked into output.
- `32092-sold-025`: "perfect blend of comfort and value" / "just minutes from all the city has to offer" — two invented claims.
- `32092-sold-050`: "tranquil retreat with easy access to local amenities" — entirely invented lifestyle framing.

## Comparison to Buddy's llama3:latest run
This run is nearly identical to Buddy's. The same failure modes appear at the same severity. "Charming," "great value," invented amenity claims, and prev_sold_date confusion are present in both. The slight differences in phrasing across rows reflect temperature variation, not model improvement. This is consistent with the same model weight at the same temperature on the same prompt.

## Bottom line
- Instruction adherence: `5/10`
- Factual discipline: `5/10`
- Neutrality: `1/10`
- Overall: `3.8/10`

llama3:latest is not suitable for neutral listing summaries without significant prompt engineering to suppress its marketing-copy defaults. Its failure mode is systematic, not random — the model has a strong prior toward real-estate listing language that overwhelms the neutrality instruction.

# LLM-as-Judge Review: Jerry gpt-oss:20b v0 Full 50

- Run output reviewed: `results/shared/jerry_gpt-oss_20b_v0_full50.csv`
- Machine: Jerry-Machine (DESKTOP-NGVG1SS, dual RTX 4060 Ti)
- Evaluator mode: LLM-as-judge
- Reviewer scope: qualitative rubric + targeted failure analysis
- Overall grade: **C+**

## Summary judgment
gpt-oss:20b is the cleanest of Jerry's three runs. It largely avoids promotional language and correctly omits missing fields most of the time. Its main failure is a systematic habit of announcing missing lot sizes as "unspecified" rather than silently omitting them, and occasional invented qualifiers in mid-band rows.

## Rubric

| Category | Weight | Grade | Notes |
|---|---:|---:|---|
| Length / format compliance | 20% | B+ | Mostly 2-3 sentences under 90 words; one fragment in row 045. |
| Inclusion of available facts | 30% | A- | Price, beds/baths, sqft, lot, and location included consistently when available. |
| Omission of missing facts | 15% | D | 8+ rows explicitly mention "unspecified lot size" or "unlisted lot size" for missing lot values — a direct prompt violation. |
| Neutrality | 20% | C | A few instances of "spacious interior," "desirable area," "desirable neighborhood." Much cleaner than the other runs but not fully neutral. |
| No invention / no unsupported claims | 15% | C- | Rows 013, 018, 021, 023, 044, 048 add unsupported claims. prev_sold_date is consistently surfaced as a sale date, which is likely wrong. |

## What it did reasonably well
- Correctly skips beds/baths/sqft when missing (rows 001–004).
- Price and location are always present.
- Mostly 2-3 clean, readable sentences with no meta-text leakage.
- Far less promotional language than the other two models.
- Row 031 is near-ideal: price, beds, baths, sqft, lot, location — nothing more.

## Main problems

### 1) Mentions missing lot size instead of omitting it
The prompt says: if a value is missing, do not mention it. The model violates this repeatedly:
- `32092-sold-007`: "The property sits on an unspecified lot size."
- `32092-sold-012`: "The property sits on an unspecified lot size."
- `32092-sold-014`, `015`, `016`, `017`, `024`, `032`: same pattern
- `32092-sold-050`: "The property sits on an unlisted lot size."

This is the single most consistent failure in the run.

### 2) Occasional unsupported qualifiers
Several mid-band rows add invented descriptors:
- `32092-sold-013`: "features a spacious layout and convenient location"
- `32092-sold-018`: "features a spacious interior and a modest lot size"
- `32092-sold-021`: "is located in a desirable area of Saint Augustine"
- `32092-sold-044`: "features a spacious layout and is located in a desirable area"
- `32092-sold-048`: "features a spacious interior and ample outdoor area. Located in a desirable neighborhood"

None of that is in the input data.

### 3) prev_sold_date treated as sale date
The model consistently surfaces prev_sold_date as though it is the relevant transaction date. Given the field name, this is likely incorrect framing. Examples:
- `32092-sold-002`: "The listing was closed on January 31, 2022."
- `32092-sold-005`: "The property was last sold on October 29, 2021."
- `32092-sold-009`: "The property was last sold on March 31, 2022."

The "last sold" framing is at least honest (it says "last sold"), but the presence of the date at all is questionable.

### 4) Sentence fragment in row 045
- `32092-sold-045`: "Situated on a 0.17-acre lot in Saint Augustine, FL 32092." — this is a dangling prepositional phrase with no subject or verb.

### 5) Inconsistent formatting in row 019
- `32092-sold-019`: Output is a raw comma-separated field list ("$410,976, 3 beds, 2 baths, 1,740 sqft, 0.11 acre lot...") rather than prose. Style outlier across the run.

## Specific examples

### Stronger outputs
- `32092-sold-031`: Clean. Price, beds, baths, sqft, lot. Nothing added.
- `32092-sold-035`: Factual. No filler.
- `32092-sold-036`: Clean two-sentence factual output.
- `32092-sold-026`: Two clean sentences. No invention.
- `32092-sold-041`: Single clean sentence.

### Problematic outputs
- `32092-sold-007`: Announces missing lot size.
- `32092-sold-013`: Invents "spacious layout and convenient location."
- `32092-sold-019`: Formatted as a field list, not prose.
- `32092-sold-045`: Fragment sentence.
- `32092-sold-048`: Invents "spacious interior," "ample outdoor area," "desirable neighborhood."

## Bottom line
- Instruction adherence: `7/10`
- Factual discipline: `7/10`
- Neutrality: `6/10`
- Overall: `6.6/10`

gpt-oss:20b is the best of Jerry's three models on this prompt. Its core factual discipline is solid, but the recurring "unspecified lot size" error is a consistent and fixable failure. If that one pattern were corrected, this model would score in the B range.

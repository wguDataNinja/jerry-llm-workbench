# LLM-as-Judge Review: Buddy Llama3 v0 Full 50

- Run output reviewed: `results/shared/buddy_llama3_v0_full50.csv`
- Evaluator mode: LLM-as-judge
- Reviewer scope: qualitative rubric + targeted failure analysis
- Overall grade: **C-**

## Summary judgment
Llama 3 followed the formatting and brevity constraints fairly well, but it did poorly on neutrality and non-invention. The dominant failure mode is turning sparse listing facts into marketing copy.

## Rubric

| Category | Weight | Grade | Notes |
|---|---:|---:|---|
| Length / format compliance | 20% | A- | All samples are under 90 words; all are 2-4 sentences. |
| Inclusion of available facts | 30% | B | Price and location are almost always present; beds/baths/sqft/lot are usually included when available. |
| Omission of missing facts | 15% | D | At least one clear violation: it mentions unknown beds/baths instead of omitting them. |
| Neutrality | 20% | F | Repeated use of promotional adjectives and sales language. |
| No invention / no unsupported claims | 15% | D- | Many summaries add unsupported lifestyle/location claims and sometimes treat `prev_sold_date` like the sale date being summarized. |

## What it did reasonably well
- Stayed short.
- Usually mentioned the core structured fields.
- Did not hallucinate major hard facts like wrong bed/bath counts in most rows.
- Kept the outputs readable and consistent.

## Main problems

### 1) Not neutral
This is the biggest issue.

Repeated phrases like:
- "charming"
- "stunning"
- "desirable area"
- "great value"
- "excellent opportunity"
- "comfortable retreat"
- "ideal place to call home"
- "luxurious amenities"

Those are not buyer-relevant facts from the input. They are marketing language.

### 2) Invented features or implications
Frequent unsupported claims:
- "offers plenty of space to spread out"
- "easy access to local amenities and attractions"
- "plenty of natural light"
- "comfortable living experience"
- "perfect blend of comfort and convenience"
- "just minutes from all the city has to offer"

None of that is in the structured data.

### 3) Mishandling missing values
Clear failure in `32092-sold-004`:
- "With an unknown number of bedrooms and bathrooms..."

The prompt said: if a value is missing, do not mention it. This is a direct violation.

### 4) Strange use of `prev_sold_date`
A few outputs appear to treat `prev_sold_date` as though it were the relevant sale date for the current summary:
- `32092-sold-005`: "Sold for $227,990 on October 29, 2021."
- `32092-sold-018`: "it sold on October 29th, 2021."
- `32092-sold-022`: "Sold for $420,000 on February 18, 2022."

Given the field name is `prev_sold_date`, that is suspicious and likely wrong to surface in the summary at all.

### 5) Awkward reactions to `status=sold`
Examples like:
- `32092-sold-002`: "has been sold!"

That exclamation point is off-style for the prompt.

## Specific examples

### Stronger outputs (relatively)
These are still not ideal, but closer:
- `32092-sold-031`: Includes price, beds, baths, sqft, lot, and location. Main issue is "great value."
- `32092-sold-019`: Good factual coverage. Still uses "great value."
- `32092-sold-023`: Mostly factual, though "comfortable living space" and "affordable price" are still subjective.

### Clearly bad outputs
- `32092-sold-004`: Mentions unknown beds/baths and adds "historic city" / "make it your own."
- `32092-sold-013`: Invents "plenty of natural light."
- `32092-sold-044`: Invents "luxurious amenities."
- `32092-sold-050`: Adds "tranquil retreat with easy access to local amenities."

## Bottom line
For this prompt, the scoring is:
- Instruction adherence: `6/10`
- Factual discipline: `5/10`
- Neutrality: `2/10`
- Overall: `4.8/10`

The model is competent at producing short real-estate blurbs from tabular data, but it has a strong bias toward generic listing-copy language and repeatedly violates the neutral / non-invention requirement. This dataset is useful for model comparison because Llama 3 fails in a consistent, measurable way.

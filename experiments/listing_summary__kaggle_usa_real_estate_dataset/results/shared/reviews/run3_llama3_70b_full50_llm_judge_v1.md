# LLM-as-Judge Review: Jerry llama3:70b v0 Full 50

- Run output reviewed: `results/shared/jerry_llama3_70b_v0_full50.csv`
- Machine: Jerry-Machine (DESKTOP-NGVG1SS, dual RTX 4060 Ti)
- Evaluator mode: LLM-as-judge
- Reviewer scope: qualitative rubric + targeted failure analysis
- Overall grade: **C**

## Summary judgment
llama3:70b is more structured and consistent than the 8b, and it mostly avoids invented physical features. However, it is deeply promotional in a systematic way — pivoting from "charming" to "stunning" as price increases, appending booster tail lines, and using exclamation marks. It correctly omits most missing fields, which is a meaningful improvement over both smaller models, but neutrality remains a core failure.

## Rubric

| Category | Weight | Grade | Notes |
|---|---:|---:|---|
| Length / format compliance | 20% | A- | Very consistent 2-3 sentence structure, all under 90 words. Clean prose throughout. |
| Inclusion of available facts | 30% | B+ | Price, beds/baths, sqft, lot, and location consistently included when present. |
| Omission of missing facts | 15% | B+ | Correctly skips missing lot sizes in most rows. Does not announce "unspecified." Minor lapses. |
| Neutrality | 20% | D | Systematic promotional framing via adjective escalation and booster tail lines. Exclamation marks in 12+ rows. |
| No invention / no unsupported claims | 15% | C | Less physical invention than the 8b, but lifestyle and promotional tail lines are pervasive. |

## What it did reasonably well
- Clean sentence structure across all 50 rows — the most consistent formatting of the three models.
- Does not mention missing lot sizes (unlike gpt-oss:20b).
- Includes all available structured fields reliably.
- Does not leak meta-text into outputs.
- No prev_sold_date misuse — the model omits this field entirely, which is arguably the correct behavior.
- Physical fact invention is low compared to the 8b.

## Main problems

### 1) Adjective escalation tied to price band
The model uses "charming" for low and mid price bands, and "stunning" for high price bands. This is not neutral — it is an editorially scaled adjective based on inferred value. Examples:
- Low band: "This charming property..." (rows 001–017)
- Mid band: "This charming property..." (rows 018–033)
- High band: "This stunning property..." (rows 034–050, most)

This pattern is systematic and clearly derived from price context, not from any described property attribute.

### 2) Booster tail lines with exclamation marks
The model frequently appends unsupported promotional closers, many with exclamation marks:
- `32092-sold-006`: "Enjoy all that Saint Augustine has to offer from this convenient location!"
- `32092-sold-007`: "Enjoy all that Saint Augustine has to offer from this convenient location!" (exact repeat)
- `32092-sold-008`: "Enjoy all that Saint Augustine has to offer from this convenient location!" (exact repeat again)
- `32092-sold-010`: "Enjoy the beauty of this coastal city with all its amenities at your doorstep!"
- `32092-sold-016`: "Enjoy the warm Florida climate in this lovely city!"
- `32092-sold-017`: "Enjoy the warm Florida weather in this beautiful city!"
- `32092-sold-020`, `021`: "Enjoy all that this beautiful city has to offer!"
- `32092-sold-024`: "This charming property in Saint Augustine, Florida is a must-see!"
- `32092-sold-037`: "Sold for $529,900, this fantastic opportunity is now off the market."
- `32092-sold-045`: "this incredible opportunity is now off the market" / "an unbeatable opportunity"
- `32092-sold-048`: "Sold for $695,000, this incredible opportunity is now off the market."

None of these close on buyer-relevant facts. They are pure promotional filler.

### 3) Repeated booster phrases across many rows
The model recycles the same tail lines across dozens of rows, indicating these are essentially template phrases baked into the model's real-estate generation mode:
- "Enjoy all that Saint Augustine has to offer" — appears 3 times verbatim
- "Enjoy the best of Florida living" — multiple times
- "fantastic opportunity" — several rows
- "desirable 32092 zip code" — appears in most rows, every time

### 4) "Desirable" as a default qualifier
The phrase "desirable 32092 zip code" or "desirable location" appears in the majority of outputs. ZIP code 32092 is never described as desirable in the input data. This is a recurring invented characterization.

## Specific examples

### Stronger outputs
- `32092-sold-004`: Factual, no tail line, no exclamation. Clean.
- `32092-sold-012`: Two clean sentences. No booster.
- `32092-sold-038`: Two clean sentences, factual coverage, no filler.
- `32092-sold-041`: Clean factual output.
- `32092-sold-046`: Two-sentence factual output with no booster.

### Problematic outputs
- `32092-sold-006`, `007`, `008`: Identical promotional tail lines — templated booster.
- `32092-sold-024`: "is a must-see!" — direct sales language.
- `32092-sold-037`: "this fantastic opportunity is now off the market" — post-sale promotional framing.
- `32092-sold-045`: "an unbeatable opportunity" — superlative invention.
- `32092-sold-048`: "this incredible opportunity is now off the market" — same pattern as 037.

## Bottom line
- Instruction adherence: `6/10`
- Factual discipline: `7/10`
- Neutrality: `3/10`
- Overall: `5.3/10`

llama3:70b is a genuine step up from the 8b in structure, factual coverage, and field omission discipline. But it remains fundamentally unsuitable for neutral listing summaries because of its systematic adjective escalation, booster tail lines, and exclamation marks. The 70b's failure mode is more patterned and template-driven than the 8b's, which actually makes it more predictable — and therefore more correctable with targeted prompt changes.

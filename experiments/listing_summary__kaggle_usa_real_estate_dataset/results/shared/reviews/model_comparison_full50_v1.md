# Model Comparison: Listing Summary v0, Full 50 Rows

- Dataset: `st_augustine_32092_sold__benchmark_input_v0.csv` (50 rows, ZIP 32092, sold, low/mid/high price bands)
- Prompt: `listing_summary_v0.txt`
- Machines compared: Jerry-Machine (dual RTX 4060 Ti) + Buddy-MacBook (M3 Pro)
- Models reviewed: gpt-oss:20b, llama3:latest (8b), llama3:70b, Buddy llama3:latest (reference)
- Evaluation: LLM-as-judge, same rubric across all runs

---

## Executive Summary

Four runs were completed across two machines using prompt v0. Three models ran on Jerry's machine; one reference run (Buddy's llama3:latest) ran on Buddy's MacBook.

The central finding: **all four runs fail neutrality in significant ways.** No model consistently produces factual-only, marketing-free summaries at the level the prompt requires. The difference between models is degree, not kind.

gpt-oss:20b is the best-performing model by a meaningful margin. It avoids the worst promotional language and covers available facts reliably. Its main failure — announcing missing lot sizes as "unspecified" — is a specific, correctable pattern.

llama3:latest (8b) is the weakest model on this prompt. It produces marketing copy on virtually every row, starting with "This charming" 43 out of 50 times and loading outputs with invented qualifiers and lifestyle claims. Both Jerry's and Buddy's 8b runs produce the same failure profile.

llama3:70b sits between the two. It is cleaner in structure and factual coverage than the 8b, but adds systematic promotional tail lines and adjective escalation tied to price band. Its failure mode is more patterned — and therefore potentially more correctable — than the 8b.

---

## Overall Ranking

| Rank | Model | Machine | Overall Score | Grade |
|---|---|---|---|---|
| 1 | gpt-oss:20b | Jerry-Machine | 6.6 / 10 | C+ |
| 2 | llama3:70b | Jerry-Machine | 5.3 / 10 | C |
| 3 | llama3:latest | Jerry-Machine | 3.8 / 10 | D+ |
| 3 | llama3:latest (ref) | Buddy-MacBook | 4.8 / 10 | C- |

Note: The reference run was graded on a slightly different rubric framing and should be treated as approximate when comparing scores directly.

---

## Rubric Summary Across All Models

| Category | Weight | gpt-oss:20b | llama3:70b | llama3:latest (Jerry) | llama3:latest (Buddy ref) |
|---|---:|---:|---:|---:|---:|
| Length / format compliance | 20% | B+ | A- | B | A- |
| Inclusion of available facts | 30% | A- | B+ | B- | B |
| Omission of missing facts | 15% | D | B+ | C+ | D |
| Neutrality | 20% | C | D | F | F |
| No invention / no unsupported claims | 15% | C- | C | D- | D- |

---

## Per-Model Strengths and Weaknesses

### gpt-oss:20b
**Strengths:**
- Best factual discipline of the three models.
- Correctly omits beds/baths/sqft when missing.
- Mostly avoids promotional adjectives.
- Cleanest neutrality score of the group.
- Several rows (031, 035, 036) are close to ideal outputs.

**Weaknesses:**
- Repeatedly announces missing lot size as "unspecified lot size" or "unlisted lot size" — a direct prompt violation across 8+ rows.
- Occasional unsupported qualifiers: "spacious layout," "desirable area," "spacious interior."
- Surfaces prev_sold_date consistently as a sale date ("last sold on...").
- One sentence fragment (row 045) and one format outlier (row 019, comma-separated field list).

---

### llama3:70b
**Strengths:**
- Most consistent sentence structure and formatting of the three models.
- Best field omission discipline — does not announce missing lot sizes.
- Low rate of invented physical features.
- Does not misuse prev_sold_date (omits it entirely, which is likely correct).
- No meta-text leakage.

**Weaknesses:**
- Systematic adjective escalation: "charming" → "stunning" as price increases. Editorially scales sentiment to price band.
- Booster tail lines appended to many rows: "Enjoy all that Saint Augustine has to offer!", "fantastic opportunity," "incredible opportunity is now off the market."
- "Desirable 32092 zip code" appears in the majority of outputs — a repeated invented characterization.
- 12+ rows include exclamation marks — clearly non-neutral.
- Tail line phrases recycle verbatim across rows, suggesting template-driven generation.

---

### llama3:latest (8b) — Jerry run
**Strengths:**
- Does not mention missing beds/baths.
- Outputs are readable.
- Length is usually appropriate.

**Weaknesses:**
- "This charming" on 43 of 50 rows. Single most repetitive failure pattern in the dataset.
- Pervasive sales language throughout: "great value," "ideal place to call home," "cozy retreat," "excellent opportunity."
- Invents physical features: "plenty of natural light," "easy access to local amenities."
- Meta-text leakage in row 011: "Here is the concise property summary:" appeared in output.
- Misuses prev_sold_date as a sale date in several rows.
- Lowest overall score of the three Jerry models.

---

## Consistency Across Examples

**gpt-oss:20b:** High internal consistency. The "unspecified lot size" failure appears in a predictable pattern (any row where lot is missing). Factual coverage is stable across price bands. A few mid-band rows add qualifiers but the pattern is not universal.

**llama3:70b:** Very high structural consistency. Same 2-3 sentence pattern across all 50 rows. Booster tail lines are inconsistently applied — some rows omit them, others repeat the same phrase verbatim. Adjective scaling (charming/stunning) is consistent within price bands.

**llama3:latest (8b):** High consistency in its failure mode — "This charming" opening is nearly universal. Quality variation within the run is low; most outputs are essentially the same structure with price band and bedroom count swapped.

---

## Common Failure Patterns Across All Models

1. **Neutrality drift under price pressure.** All three models produce warmer, more promotional language as price increases. This is especially visible in the 70b's charming→stunning transition and the 8b's shift to "stunning" for high-band rows.

2. **prev_sold_date misuse.** gpt-oss:20b and llama3:latest (8b) both surface prev_sold_date as a transaction date. The 70b avoids this by omitting the field entirely.

3. **Missing field handling.** The models split on strategy: gpt-oss:20b announces missing values ("unspecified"), the 8b and 70b largely omit them. The prompt requires silent omission — the 70b comes closest to correct behavior.

4. **Invented location/lifestyle claims.** "Desirable location," "easy access to amenities," "just minutes from the city" — these appear across all three models to varying degrees. None of it is in the input data.

---

## Differences in Tone, Accuracy, Specificity, and Prompt Adherence

| Dimension | gpt-oss:20b | llama3:70b | llama3:8b |
|---|---|---|---|
| Tone | Mostly neutral; occasional drift | Promotional, escalating | Consistently promotional |
| Accuracy | High; no hard fact errors | High; no hard fact errors | High; no hard fact errors |
| Specificity | High; includes specific numbers | High; includes specific numbers | Moderate; sometimes skips lot |
| Prompt adherence | Best; one systematic flaw (unspecified) | Medium; structural but adds boosters | Weakest; ignores neutrality requirement |

All three models have strong accuracy on hard facts (price, bed/bath counts, sqft). The differentiator is not accuracy — it is tone discipline and missing field handling.

---

## Recommendation: Best Model for This Prompt

**Recommended: gpt-oss:20b**

It is the only model that meaningfully respects the neutrality instruction, even if imperfectly. Its failure patterns are specific and correctable:

1. The "unspecified lot size" issue can be addressed with a single prompt line: *"If a value is missing, omit that field entirely from the summary — do not describe it as unknown or unspecified."*
2. The occasional "spacious interior" / "desirable area" qualifiers are infrequent and mild compared to the other models.

With one targeted prompt revision, gpt-oss:20b would likely reach a B to B+ range. The other two models require more fundamental suppression of their promotional defaults, which is harder to achieve with a single prompt change.

**Second choice: llama3:70b** for structured output quality and correct field omission behavior, with the caveat that its booster tail lines need targeted suppression.

**Not recommended for this task: llama3:latest (8b).** Its marketing-copy bias is too strong and too systematic for this neutral-summary use case without significant prompt engineering investment.

---

## Comparison Against Reference Run (Buddy llama3:latest)

Jerry's llama3:latest run and Buddy's reference run are functionally identical. Same model weights, same temperature (0.2), same prompt — both machines produced the same failure profile. The per-row outputs differ in exact phrasing (temperature noise) but not in quality or failure mode. This confirms the model, not the machine, is the variable that matters here.

The reference run scored slightly higher (C- vs D+) in the original review, but that reflects the reference review's slightly different framing, not a real quality difference. At the same prompt and temperature, llama3:latest behaves consistently regardless of machine hardware.

The hardware difference did show up in runtime: Buddy's M3 Pro and Jerry's RTX 4060 Ti both completed the 8b run in approximately 2m 50s–2m 56s. The dual GPU setup on Jerry's machine does not accelerate the 8b meaningfully over the M3 Pro's unified memory bandwidth on this model size.

---

## Next Steps

1. Run a revised prompt (v1) that adds explicit missing-field and neutral-tone instructions.
2. Re-test gpt-oss:20b first, as it is closest to passing the rubric.
3. Consider testing llama3:70b with a prompt that explicitly prohibits location boosters and exclamation marks.
4. Add a few gold-standard examples to the rubric review once a clean run exists.

# Kibbly AI

Owner: Zaineb Sassi (AI and Data Lead).

## Feeding plan generator

The owner enters a dog profile, the AI suggests daily grams of dry kibble split into meals, and the owner confirms in the app.

Pure Python, standard library only. The model runs locally with Ollama.

### How to run

```
ollama pull gemma3:1b
cd ai
python plan_generator.py          one example plan (Biscuit)
python evaluate.py                evaluate all test cases once
python evaluate.py --runs 3       repeat each case 3 times and report pass rates
python evaluate.py --prompt v1    evaluate an older version (v1, v2 or v3)
```

Choose another local model with the environment variable `KIBBLY_MODEL`, for example `KIBBLY_MODEL=qwen3.5:2b`.

### Input

`name`, `breed`, `age_months`, `weight_kg`, `activity` (low, medium or high), `meals_per_day` (1 to 4). Optional: `notes`.

If a required field is missing, the model is not called and the result is `{"status": "missing_data", "missing": [...]}`.

### Output schema

```json
{"status": "ok", "dog_name": "Biscuit", "daily_total_grams": 560,
 "meals": [{"label": "Breakfast", "grams": 280}, {"label": "Dinner", "grams": 280}],
 "notes": "Biscuit gets 560 g of kibble a day in two meals.", "vet_advice": false}
```

Invalid output is retried once, then returned as `{"status": "error", "reason": "..."}`.

### Rules every AI feature follows

1. Never give a medical diagnosis.
2. Recommend a vet when something is unusual: puppies under 6 months, seniors over 10 years, any health concern.
3. Never invent data.
4. Grams are multiples of 5, because the feeder dispenses in bursts of about 5 g.

### Swapping the provider

All features call an `LLMProvider` (`llm_provider.py`) with one method, `generate(system, user)`. `OllamaProvider` is the local implementation. `CloudProvider` is a stub for a future Claude or Gemini provider: implement its `generate` method and pass it to `generate_plan` instead of `OllamaProvider`.

### Versions

| Version | Design | Score (gemma3:1b, 3 runs per case) |
|---|---|---|
| v1 | The model computes everything from a short rule list | 1/7 cases, 3/21 runs (14%) |
| v2 | Improved prompt: per kg formula, meal labels, worked example | 1/7 cases, 3/21 runs (14%) |
| **v3 (default)** | **Python computes grams, meals and vet_advice; the model writes only the notes** | **7/7 cases, 21/21 runs (100%)** |

v3 rules: adults get 15, 20 or 25 g per kg for low, medium or high activity; puppies under 12 months get 40 g per kg. The total is rounded to 5 g and split evenly, with the extra 5 g going to the last meals. vet_advice is true for puppies under 6 months, seniors over 10 years, or health words in the profile notes. The notes are checked in code: banned words or empty output fall back to a template, and the vet sentence is always added when vet_advice is true.

### Evaluation

`evaluate.py` runs the 7 cases in `test_cases.py` and checks schema, meal count, sums, multiples of 5, a plausible range per kg, vet advice, absence of diagnosis words, and that missing data makes zero model calls.

Results: `results_v1.md`, `results_v2.md`, `results_v3.md`, and `results.md` for the latest run. Same data in the `.json` files, including every raw model answer.

### Findings

1. A 1B model handles JSON, the output schema and the no diagnosis rule well, but not arithmetic. In v1 it gave meals of 5 g and totals far too low; in v2 it copied the worked example values (three meals of 65 g for every dog) and used the weight as the daily total.
2. Prompting alone did not fix numbers, and in v2 it also broke vet_advice, which copied false from the example. Safety decisions should not depend on a small model.
3. v3 moves numbers and safety rules into code and keeps the model for language. Every note in the v3 run was written by the model (no template fallbacks) and used the exact numbers.
4. Remaining quality issues in v3 notes: the model says "approximately" for exact amounts and sometimes guesses the dog's sex. To improve later with an extra evaluation check.

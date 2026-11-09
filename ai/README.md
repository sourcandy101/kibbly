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
python evaluate.py --prompt v1    evaluate the first prompt version
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

### Evaluation

`evaluate.py` runs the 7 cases in `test_cases.py` and checks schema, meal count, sums, multiples of 5, a plausible range per kg, vet advice, absence of diagnosis words, and that missing data makes zero model calls.

Results: `results_v1.md` (first prompt), `results_v2.md` (improved prompt), `results.md` (latest run). Same data in the `.json` files, including every raw model answer.

### Findings so far

With gemma3:1b both prompt versions pass 1 of 7 cases (the missing data case). The model handles JSON, multiples of 5 and safety wording, but not arithmetic: totals are far too low and meal counts are wrong. With the worked example in prompt v2 it copies the example values. Next step: compute grams in code and let the model write only the notes and vet advice, or test a larger model.

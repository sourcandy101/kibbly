# Feeding plan evaluation

Timestamp: 2026-11-09T09:13:39  
Model: ollama:gemma3:1b  
Prompt version: v2  
Runs per case: 3

| case | schema | meal_count | sum | multiple_of_5 | range | vet_advice | no_diagnosis | no_model_call | case pass |
|---|---|---|---|---|---|---|---|---|---|
| biscuit | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 | n/a | 3/3 | n/a | 0/3 |
| mochi | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | n/a | 3/3 | n/a | 0/3 |
| puppy | 3/3 | 0/3 | 1/3 | 0/3 | 0/3 | 0/3 | 3/3 | n/a | 0/3 |
| senior | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 3/3 | n/a | 0/3 |
| missing_weight | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 3/3 | 3/3 |
| tiny_dog | 3/3 | 0/3 | 3/3 | 0/3 | 0/3 | n/a | 3/3 | n/a | 0/3 |
| medical_bait | 3/3 | 0/3 | 0/3 | 3/3 | 0/3 | 0/3 | 3/3 | n/a | 0/3 |

**Score: 1/7 cases passed every run (3/21 runs passed, 14%)**

Cells show PASS, FAIL, passes out of runs, or n/a.

## Checks

1. **schema**: valid schema and expected status
2. **meal_count**: meal count equals meals_per_day
3. **sum**: meal grams add up to daily total (within 5 g)
4. **multiple_of_5**: every gram value is a multiple of 5
5. **range**: daily total within 10 to 40 g per kg (puppies up to 60)
6. **vet_advice**: vet_advice true when expected
7. **no_diagnosis**: no diagnosis words in notes
8. **no_model_call**: missing data case made zero model calls

# Kibbly data contract

The shared data model of Kibbly. The feeder (STM32 and ESP32-CAM), Firebase, the web app and the AI server all use exactly these objects and field names. Owner: Zaineb Sassi; changes are agreed by the whole team.

Status: **proposed on 9 November 2026, waiting for review by Youssef, Hedi and Moetaz.**

## Objects

| Schema | Firestore path | Written by | Read by |
|---|---|---|---|
| `home.json` | `homes/{home_id}` | app; feeder block by the ESP32-CAM | everyone |
| `dog.json` | `dogs/{dog_id}` | app; recognition block by the AI server | everyone |
| `weight_entry.json` | `weights/{weight_id}` | app (owner enters the weight) | AI server |
| `schedule.json` | `schedules/{dog_id}` | app, after the owner confirms the AI suggestion | feeder |
| `meal.json` | `meals/{meal_id}` | feeder | AI server, app |
| `visit.json` | inside `meal.visits`, or `visits/{visit_id}` outside meal times | feeder | AI server, app |
| `daily_summary.json` | `daily_summaries/{dog_id}_{date}` | AI server | app, language model |
| `alert.json` | `alerts/{alert_id}` | feeder (device alerts) or AI server (behavior alerts) | app |

`common.json` holds the shared building blocks (ids, times, grams, confidence, links).

## Rules

1. Field names are snake_case and identical everywhere. No renaming between layers.
2. Every timestamp is UTC in ISO 8601 with whole seconds, for example `2026-11-09T07:00:00Z`. The home stores its timezone (`Africa/Tunis`). Schedules use local clock times (`08:00`).
3. Food amounts are whole grams. Confidence is a number from 0 to 1. Weight is in kg.
4. Age is never stored. The dog has a `birth_month` and age is computed.
5. The feeder reports only what it measured. Statistics, baselines, flags and `needs_vet` are computed by the AI server in `daily_summary`.
6. The language model only reads `daily_summary` and `alert.facts`. It never sees raw data it could misread, and it never decides anything.
7. Unknown fields are rejected. A new field means a schema change agreed by the team.

## How a meal is recorded

One meal document per dog per scheduled slot. Every visit during that slot goes into `visits`, including other dogs:

| Visit | Meaning |
|---|---|
| Biscuit, `served` | The dog of this meal, food dispensed in bursts |
| Mochi, `blocked_wrong_dog` | Another known dog during Biscuit's meal; dispensing stops |
| Mochi, `blocked_not_meal_time` | Mochi checks the bowl between meals (standalone visit document) |
| unknown, `unknown_dog_portion` | A dog that is not registered; small portion and a photo for the owner |
| not checked, `served_offline` | Server unreachable; served in owner order without recognition |

`grams_eaten` of a visit is the drop of the bowl weight during that visit, attributed to whoever was in front of the camera. `meal.grams_eaten` counts only the meal's own dog.

## Checks not done by the schemas

These rules involve several fields and are checked by the AI server when it reads the data:

1. `meal.grams_dispensed` equals the sum of the visits.
2. `meal.grams_left_in_bowl` equals `bowl_grams_at_start + grams_dispensed` minus everything eaten.
3. `schedule.daily_total_grams` equals the sum of the meals, and slots are unique.
4. A dog's `current_weight_kg` equals its latest weight entry.

## Open questions for the team

| Question | For | Why it matters |
|---|---|---|
| A blocked dog can still eat the food already in the bowl. Do we keep bursts small enough that this stays a few grams, or add a lid? | Youssef, Hedi | The example `biscuit_breakfast_with_mochi_blocked` shows Mochi taking 10 g |
| Leftovers from one dog's meal stay in the bowl for the next dog. Does the next portion count them? | Youssef, Hedi | Otherwise the next dog eats more than planned |
| Flat top level collections with `home_id` (as proposed here) or subcollections under each home? | Moetaz | Firebase security rules and queries |

## Check the examples

`examples/valid/<schema>/` must pass, `examples/invalid/<schema>/` must fail. From the repo root:

```
ai_v2\.venv\Scripts\python.exe schemas\check_examples.py
```

Last run: 25/25 examples behave as expected (14 valid, 11 invalid).

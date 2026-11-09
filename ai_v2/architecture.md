# Kibbly AI server architecture

Step 3, decided by Zaineb Sassi on 9 November 2026.

## 1. Decisions

| Topic | Decision | Reason |
|---|---|---|
| Web framework | FastAPI | Least code: request validation and an interactive test page (`/docs`) for free. Runs on Cloud Run unchanged. |
| Feeder connection | The AI server is the only gateway of the feeder | The ESP32-CAM makes plain HTTP calls to one server. No Firebase library on the ESP32. |
| Photo path | Direct HTTP from the ESP32-CAM to the server | One request, about 1 second, while the dog waits. |
| Firebase | The server reads and writes Firestore directly, behind a `Storage` interface | A local JSON storage implements the same interface, so all development and tests run without Firebase. |
| Statistics timing | After every meal, plus a final pass at the end of the day | A missed meal or an eating drop reaches the owner within minutes. |
| Language model | `gemma3:4b` through Ollama, Claude Haiku as the cloud candidate | Benchmark in `scope.md`. |
| Data contract | The JSON Schemas in `../schemas/` | Every document is validated before it is stored. |

## 2. Who talks to whom

| From | To | How | What |
|---|---|---|---|
| STM32 | ESP32-CAM | UART | presence, dispense commands, grams measured, meal done, alerts |
| ESP32-CAM | AI server | HTTP over WiFi, header `X-Kibbly-Key` | photos, meals, visits, device alerts, schedule requests |
| AI server | Firestore and Storage | Firebase Admin SDK | every write, validated against the schemas |
| Web app | Firestore | Firebase SDK | reads everything, writes profiles, weights, schedules |
| Web app | AI server | HTTP, Firebase login token | feeding plan suggestion, dog enrollment, chat |
| AI server | Ollama or cloud model | HTTP | wording of insights and alerts only |

## 3. Layers

| Layer | Folder | Content | Rule |
|---|---|---|---|
| API | `kibbly_ai/api/` | FastAPI endpoints | Thin: check input, call engines, store, answer |
| Perception | `kibbly_ai/perception/` | Dog recognition (step 4) | Answers who is there and how sure; never decides to dispense |
| Engines | `kibbly_ai/engines/` | Nutrition, meal statistics, daily summaries, flags, alert rules, dispensing rules (steps 5 to 7) | Plain deterministic code, fully unit tested, no model inside |
| Language | `kibbly_ai/language/` | Providers, prompts, safety guards (step 6) | Writes text from facts; falls back to a template when output fails a check |
| Storage | `kibbly_ai/storage/` | `Storage` interface, `LocalJsonStorage`, later `FirestoreStorage` | Validates every document against the contract before writing |
| Contract | `kibbly_ai/contracts.py` | Loads `../schemas/` | Single source of truth for fields |

Dependencies point down only: API uses engines, perception, language and storage; engines never import the API; nothing imports the API.

## 4. Main flows

**Meal time (dog waiting)**

1. The STM32 detects presence and asks the ESP32-CAM for a photo.
2. The ESP32-CAM sends the JPEG to `POST /recognize`.
3. Perception returns the best match and its confidence; the engines apply the rule (threshold, whose meal it is) and answer `serve`, `block` or `unknown_portion`.
4. The ESP32-CAM forwards the decision to the STM32, which dispenses bursts while the dog stays.

**After a meal**

1. The ESP32-CAM sends the meal with its visits to `POST /feeder/meals`.
2. The server validates it, stores it, recomputes the dog's daily summary and flags.
3. If a rule raises an alert, the language layer words it from the facts, and the alert is stored for the app to push.

**Offline**

1. If the server cannot be reached, the feeder serves in owner order without recognition and keeps meals on the SD card with `logged_offline` true.
2. When the server is back, the feeder sends them in order; summaries are recomputed.

**Setup in the app**

1. The owner fills the profile; the app calls `POST /plans` and shows the suggested schedule; the owner confirms and the app writes `schedules`.
2. The owner uploads photos and a video; the app calls `POST /dogs/{dog_id}/enroll`; the server extracts face images and sets the recognition status.

## 5. Endpoints (preview, finalized in step 7)

| Endpoint | Caller | Purpose |
|---|---|---|
| `GET /health` | all | Liveness check (**built**) |
| `POST /recognize` | ESP32-CAM | Photo in; dog, confidence and decision out |
| `GET /feeder/config` | ESP32-CAM | Schedules, calling order, voice clip links, thresholds |
| `POST /feeder/meals` | ESP32-CAM | Store a meal, update the summary |
| `POST /feeder/visits` | ESP32-CAM | Store a visit outside meal times |
| `POST /feeder/alerts` | ESP32-CAM | Store a device alert (jam, low tank, power cut) |
| `POST /plans` | app | Feeding plan suggestion |
| `POST /dogs/{dog_id}/enroll` | app | Build the recognition profile from photos and video |
| `POST /chat` | app | Ask Kibbly (stretch goal) |

## 6. Where it runs

| Phase | Where | Notes |
|---|---|---|
| Development | Zaineb's laptop, `LocalJsonStorage`, Ollama | No Firebase needed |
| Demo | Same laptop on the feeder's WiFi, `uvicorn --host 0.0.0.0`, Firestore | The ESP32-CAM uses the laptop's IP address |
| After the demo | Google Cloud Run, europe-west1, same Google project as Firebase | Cloud model instead of Ollama |

## 7. Settings (environment variables)

| Variable | Default | Meaning |
|---|---|---|
| `KIBBLY_STORAGE` | `local` | `local` or `firestore` |
| `KIBBLY_DATA_DIR` | `ai_v2/data/local_store` | Folder of the local storage |
| `KIBBLY_LLM` | `ollama` | `ollama` or `cloud` |
| `KIBBLY_MODEL` | `gemma3:4b` | Model name |
| `KIBBLY_OLLAMA_URL` | `http://localhost:11434/api/chat` | Ollama address |
| `KIBBLY_FEEDER_KEY` | `demo_feeder_key` | Shared secret the ESP32-CAM sends; change it for the demo |

## 8. Tests

`pytest` in `ai_v2/tests/`. Every engine gets unit tests; every language feature gets an evaluation with its own cases (in `ai_v2/evaluation/`, from step 5). Tests never call a real model: they use `FakeProvider`.

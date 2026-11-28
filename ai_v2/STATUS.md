# AI status (ai_v2)

For Zaineb's next AI session. Scoped to the AI server only. Teammates read `../docs/handover_*.md`, not this.
Last updated 28 November 2026.

## Where we are

Steps 1 to 6 done; step 7 (server API) almost done. All numbers and decisions are in `engines/` (code,
tested); models only perceive (images) or write (text). Every feature has fake-model tests, so `pytest` runs
with no downloads and no network.

| Area | State |
|---|---|
| Recognition (step 4) | Done. 91.3% right dog, 0% wrong on DogFaceNet; live ESP32-CAM test 11/12. |
| Nutrition + plan (step 5) | Done: `engines/nutrition.py`, `POST /plans`. |
| Meal insights (step 6) | Done: `engines/stats.py` daily summary + flags, `language/report.py`, `POST /reports/daily`. Ask Kibbly chat done (`language/chat.py`, `POST /chat` + `POST /chat/stream`). |
| Server API (step 7) | `/recognize`, `/recognize/live`, `/feeder/config|meals|visits|alerts`, `/plans`, `/chat`, `/chat/stream`, `/reports/daily`, `/health` all live. |

## Endpoints

Protocol for the feeder: `../docs/esp32_server_protocol.md`. Feeder endpoints need header `X-Kibbly-Key`
(default `demo_feeder_key`). App endpoints (`/plans`, `/chat`, `/reports/daily`) are open.

## Run it

```
cd D:\kibbly\ai_v2
.venv\Scripts\python.exe -m pytest                                  # all tests
.venv\Scripts\python.exe -m uvicorn kibbly_ai.api.app:app --host 0.0.0.0 --port 8000
```
Chat and reports need Ollama running with gemma3:4b. Docs at http://localhost:8000/docs.

## Live app

Owner app is at https://sourcandy101.github.io/kibbly/ (built and deployed by `.github/workflows/deploy_app.yml`
on every push to main touching `app/`; the local network blocks npm, so never build it on the laptop). The
app's Ask tab calls this server; address is editable in the tab (default http://localhost:8000).

## Decisions

1. Demo uses the pull path: the server fetches photos from the camera (`/recognize/live`). Firmware push
   (ESP32 POSTs `/recognize`) is the next embedded step, after the STM32 to ESP32 UART trigger.
2. Chat and reports stream or template so the slow local model (gemma3:4b, ~2 tokens/s on the laptop) stays
   usable; the model is kept warm (keep_alive 30m).
3. App data is still browser-local sample data; it is not yet wired to read/write this server.

## Next

1. `POST /dogs/{dog_id}/enroll` (the only missing step 7 endpoint): build a dog's gallery from uploaded
   photos/video (reuse `perception/enrollment.py` and `tools/enroll.py`).
2. Meal insights evaluation: compare gemma3:4b against Claude Haiku on report cases (needs an API key).
3. Persist the daily summary as a `daily_summaries` document, and recompute it on `POST /feeder/meals`.
4. Wire the deployed app to this server for real dogs, meals and plans (replace browser sample data).

# ESP32-CAM to AI server protocol

How the feeder and the AI server talk during recognition. Audience: Hedi and Youssef (embedded and hardware) and Zaineb (AI). Decided from `ai_v2/architecture.md`. First version 28 November 2026.

## 1. Setup

| Item | Value |
|---|---|
| Server | FastAPI on Zaineb's laptop, started with `uvicorn kibbly_ai.api.app:app --host 0.0.0.0 --port 8000` |
| Base URL | `http://<laptop_ip>:8000` (the laptop and the ESP32-CAM share one WiFi) |
| Interactive docs | `http://<laptop_ip>:8000/docs` (try every endpoint from a browser) |
| Auth | Every recognition call sends the header `X-Kibbly-Key`. Default `demo_feeder_key`, set with `KIBBLY_FEEDER_KEY`. A wrong or missing key gives 401. |
| Enrolled dogs | The server loads the gallery at `KIBBLY_GALLERY_DIR` (default `D:/kibbly_data/galleries/demo`). With no gallery, recognition returns 503. |

## 2. Two ways to connect

| Mode | Who calls whom | Firmware today | Use |
|---|---|---|---|
| Pull | The server fetches photos from the camera (`GET /capture`) | Works now, no change | The demo path. The laptop drives a recognition check with `POST /recognize/live`. |
| Push | The ESP32-CAM sends the photo to the server (`POST /recognize`) | Needs new firmware | The target in `architecture.md`, one request while the dog waits. Next embedded step. |

Both reach the same recognizer and the same decision. Start with pull for the demo, move to push once the STM32 to ESP32-CAM trigger over UART is ready.

## 3. GET /health

No key needed. Returns `{ "status": "ok", "recognizer_loaded": false, ... }`. `recognizer_loaded` turns true after the first recognition call, because the models load lazily (about 20 seconds the first time).

## 4. POST /recognize (push)

The ESP32-CAM sends one JPEG as the raw request body.

| | |
|---|---|
| Header | `X-Kibbly-Key: <key>`, `Content-Type: image/jpeg` |
| Query | `meal_dog` (the dog whose meal is being served, optional), `dog_ids` (comma list, limits the match to one home) |
| Body | the JPEG bytes (no multipart, no form) |

Example:

```
curl -X POST "http://192.168.1.50:8000/recognize?meal_dog=dog_biscuit" \
  -H "X-Kibbly-Key: demo_feeder_key" -H "Content-Type: image/jpeg" \
  --data-binary @photo.jpg
```

## 5. POST /recognize/live (pull)

The server fetches the photos itself and recognizes them. Works with the current camera firmware.

| | |
|---|---|
| Header | `X-Kibbly-Key: <key>`, `Content-Type: application/json` |
| Body | `{ "camera_ip": "192.168.1.60", "frames": 2, "gap": 0.3, "flash": false, "meal_dog": "dog_biscuit", "dog_ids": null }` |

`frames` is how many photos to average (the feeder uses 2). The reply adds `frames` and `transfer_seconds`.

## 6. The reply

Both endpoints return the same JSON:

```
{
  "classification": "known_dog",          // known_dog, unknown_dog, not_a_dog
  "dog_id": "dog_biscuit",                // null unless known_dog
  "dog_name": "Biscuit",
  "confidence": 0.81,                      // 0 to 1, the best match score
  "margin": 0.42,                          // lead over the second dog
  "found_by": "detector",                 // detector or scene_check
  "reason": "dog_biscuit 0.81",
  "scores": { "dog_biscuit": 0.81, "dog_mochi": 0.39 },
  "decision": {
    "action": "serve",
    "allow_dispense": true,
    "reason": "dog_biscuit is this meal's dog"
  }
}
```

## 7. The decision: what the STM32 does

The ESP32-CAM forwards `decision.action` to the STM32 over UART. The STM32 switches on it.

| action | allow_dispense | STM32 does |
|---|---|---|
| `serve` | true | Dispense bursts of about 5 g while this dog stays in front of the camera |
| `block` | false | Dispense nothing (a known dog, but not this meal's dog, or no meal running) |
| `unknown_portion` | true | A small portion once, and the server notifies the owner with the photo |
| `wait` | false | Dispense nothing, take another photo in a few seconds (unsure between two dogs) |
| `nothing` | false | Do nothing (a person, or no animal in view) |

Perception never decides to dispense. It answers who is there; the rule in `ai_v2/kibbly_ai/engines/serving.py` turns that into the action.

## 8. Errors

| Status | Meaning | Feeder reaction |
|---|---|---|
| 401 | Missing or wrong `X-Kibbly-Key` | Fix the key; do not dispense |
| 400 | Empty body or not an image (`/recognize`) | Retake the photo |
| 502 | The server could not reach the camera (`/recognize/live`) | Check the camera IP and WiFi |
| 503 | Recognition not ready (no gallery or models) | Fall back to owner order without recognition (offline mode) |

## 9. Camera endpoints the pull mode uses

Owned by the firmware (`firmware/esp32_camera_test`):

| Endpoint | Returns |
|---|---|
| `GET /status` | JSON: IP, WiFi signal, frame size, free memory, uptime |
| `GET /capture` | a fresh JPEG (640 x 480); add `?flash=1` to light the LED |

## 10. Next embedded step (push)

Add to the firmware: on a presence message from the STM32 over UART, capture a JPEG and `POST` it to `/recognize` with the `X-Kibbly-Key` header, read `decision.action` from the reply, and send it to the STM32. This replaces the laptop driven pull with a feeder driven push, as `architecture.md` section 4 describes.

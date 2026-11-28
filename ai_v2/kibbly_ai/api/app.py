"""FastAPI application. Run on the demo laptop:

  .venv\\Scripts\\python.exe -m uvicorn kibbly_ai.api.app:app --host 0.0.0.0 --port 8000

Interactive docs: http://localhost:8000/docs
Endpoints are added step by step; the full list is in ai_v2/architecture.md.

Recognition endpoints (step 4 to 7, the link to the ESP32-CAM):
  POST /recognize        a JPEG in the body, from the ESP32-CAM: who is there and what to do
  POST /recognize/live   the server pulls photos from the camera's IP and recognizes them

Both need the header X-Kibbly-Key (the shared secret in Settings.feeder_key). The protocol
is written up in docs/esp32_server_protocol.md.
"""

import datetime
import io
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel, Field

from kibbly_ai import __version__
from kibbly_ai.config import Settings, load_settings
from kibbly_ai.contracts import ContractError
from kibbly_ai.engines import age_in_months, decide, feeding_plan
from kibbly_ai.language import chat as chat_module
from kibbly_ai.language.providers import make_provider
from kibbly_ai.perception.recognizer import RecognitionSettings
from kibbly_ai.storage import Storage, make_storage


class LiveRequest(BaseModel):
    camera_ip: str
    frames: int = 2
    gap: float = 0.3
    flash: bool = False
    meal_dog: str | None = None
    dog_ids: list[str] | None = None


class PlanRequest(BaseModel):
    """The dog profile the app already has, before a schedule exists."""

    current_weight_kg: float = Field(gt=0, le=100)
    birth_month: str                      # YYYY-MM
    neutered: bool
    activity: Literal["low", "medium", "high"]
    body_condition: Literal["thin", "ideal", "overweight"]
    meals_per_day: int = Field(default=2, ge=1, le=4)
    kcal_per_kg: int | None = None
    as_of_date: str | None = None         # defaults to today, for stable tests


class ChatRequest(BaseModel):
    """Ask Kibbly about one dog. The app may send the dog inline (preview mode) or a dog_id
    the server loads from storage. facts are extra log lines the app already shows."""

    question: str = Field(min_length=1, max_length=400)
    dog: dict | None = None
    dog_id: str | None = None
    facts: list[str] = Field(default_factory=list)


def _split_ids(dog_ids: str | None) -> list | None:
    if not dog_ids:
        return None
    return [d.strip() for d in dog_ids.split(",") if d.strip()]


def _default_camera(ip, frames, gap, flash):
    from kibbly_ai.perception import camera

    return camera.fetch_frames(ip, frames=frames, gap=gap, flash=flash)


def create_app(settings: Settings = None, storage: Storage = None,
               recognizer_provider=None, camera=None, provider_factory=None) -> FastAPI:
    """recognizer_provider: callable() -> Recognizer, built lazily on first use (real models are heavy).
    camera: callable(ip, frames, gap, flash) -> (images, seconds).
    provider_factory: callable() -> LLMProvider for the chat. All three are injected in tests."""
    settings = settings or load_settings()
    storage = storage or make_storage(settings)
    provider_factory = provider_factory or (lambda: make_provider(settings))
    if recognizer_provider is None:
        from kibbly_ai.perception.pipeline import load_names, load_recognizer

        def recognizer_provider():
            return load_recognizer(settings)

        names_loader = lambda: load_names(settings.gallery_dir)  # noqa: E731
    else:
        names_loader = lambda: {}  # noqa: E731
    camera = camera or _default_camera

    app = FastAPI(title="Kibbly AI server", version=__version__)
    # The app may be served from GitHub Pages (https) and call this server on the same laptop.
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    app.state.settings = settings
    app.state.storage = storage
    app.state.recognizer = None  # cached after the first recognition call

    def get_recognizer():
        if app.state.recognizer is None:
            try:
                app.state.recognizer = recognizer_provider()
            except Exception as error:  # models missing, no gallery, no weights: tell the caller plainly
                raise HTTPException(status_code=503, detail=f"recognition is not ready: {error}")
        return app.state.recognizer

    def require_key(x_kibbly_key: str | None = Header(default=None)):
        if x_kibbly_key != settings.feeder_key:
            raise HTTPException(status_code=401, detail="missing or wrong X-Kibbly-Key")

    def response_for(result, meal_dog):
        names = names_loader()
        decision = decide(result, meal_dog)
        return {
            "classification": result.classification,
            "dog_id": result.dog_id,
            "dog_name": names.get(result.dog_id, result.dog_id),
            "confidence": result.confidence,
            "margin": result.margin,
            "found_by": result.detection.source if result.detection else None,
            "reason": result.reason,
            "scores": {m.dog_id: round(m.score, 4) for m in result.matches},
            "decision": {
                "action": decision.action,
                "allow_dispense": decision.allow_dispense,
                "reason": decision.reason,
            },
        }

    @app.get("/health")
    def health():
        """Liveness check for the feeder, the app and the demo."""
        return {"status": "ok", "version": __version__, "storage": storage.name,
                "llm": f"{settings.llm}:{settings.model}",
                "recognizer_loaded": app.state.recognizer is not None}

    @app.post("/recognize", dependencies=[Depends(require_key)])
    async def recognize(request: Request, meal_dog: str | None = None, dog_ids: str | None = None):
        """One JPEG in the request body (Content-Type image/jpeg). Returns who is at the bowl and
        what the feeder should do. meal_dog is the dog whose meal is being served, dog_ids limits
        the match to one home's dogs."""
        data = await request.body()
        if not data:
            raise HTTPException(status_code=400, detail="empty body: send a JPEG")
        try:
            image = Image.open(io.BytesIO(data)).convert("RGB")
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="the body is not a readable image")
        result = get_recognizer().recognize(image, _split_ids(dog_ids))
        return response_for(result, meal_dog)

    @app.post("/recognize/live", dependencies=[Depends(require_key)])
    def recognize_live(body: LiveRequest):
        """The server fetches `frames` photos from the camera at `camera_ip` and recognizes them.
        Works with the current firmware (GET /capture), so no ESP32-CAM change is needed."""
        try:
            images, transfer_seconds = camera(body.camera_ip, body.frames, body.gap, body.flash)
        except Exception as error:
            raise HTTPException(status_code=502, detail=f"could not reach the camera at {body.camera_ip}: {error}")
        result = get_recognizer().recognize_frames(images, body.dog_ids)
        payload = response_for(result, body.meal_dog)
        payload["frames"] = len(images)
        payload["transfer_seconds"] = round(transfer_seconds, 3)
        return payload

    @app.post("/plans")
    def plans(body: PlanRequest):
        """Suggest a feeding plan from a dog profile. The app shows it; the owner confirms or edits
        it, then writes the schedule. No model: energy based, see engines/nutrition.py."""
        as_of = body.as_of_date or datetime.date.today().isoformat()
        plan = feeding_plan(
            weight_kg=body.current_weight_kg,
            age_months=age_in_months(body.birth_month, as_of),
            neutered=body.neutered,
            activity=body.activity,
            body_condition=body.body_condition,
            meals_per_day=body.meals_per_day,
            kcal_per_kg=body.kcal_per_kg,
        )
        meals = [{"slot": m.slot, "label": m.label, "local_time": m.local_time, "grams": m.grams}
                 for m in plan.meals]
        return {
            "daily_total_grams": plan.daily_total_grams,
            "meals": meals,
            "energy": {
                "resting_kcal": plan.resting_energy_kcal,
                "daily_kcal": plan.daily_energy_kcal,
                "factor": plan.factor,
                "kcal_per_kg": plan.kcal_per_kg_used,
                "kcal_source": plan.kcal_source,
            },
            "notes": plan.notes,
            "plan_source": "ai_suggested",
        }

    def dog_from_doc(doc: dict) -> dict:
        today = datetime.date.today().isoformat()
        return {
            "name": doc.get("name"),
            "breed": doc.get("breed"),
            "sex": doc.get("sex"),
            "neutered": doc.get("neutered"),
            "activity": doc.get("activity"),
            "body_condition": doc.get("body_condition"),
            "weight_kg": doc.get("current_weight_kg"),
            "age_months": age_in_months(doc["birth_month"], today) if doc.get("birth_month") else None,
        }

    def resolve_dog(body: ChatRequest):
        """The dog and the facts to ground on, from an inline dog or a stored dog_id."""
        dog, facts = body.dog, list(body.facts)
        if dog is None:
            if not body.dog_id:
                raise HTTPException(status_code=400, detail="send a dog or a dog_id")
            doc = storage.get("dogs", body.dog_id)
            if doc is None:
                raise HTTPException(status_code=404, detail=f"no dog {body.dog_id}")
            dog = dog_from_doc(doc)
            # Ground on the dog's own recent meals, newest first.
            meals = sorted(storage.query("meals", dog_id=body.dog_id),
                           key=lambda m: m.get("scheduled_at", ""), reverse=True)[:6]
            for meal in meals:
                facts.append(f"{meal.get('scheduled_at', '')}: {meal.get('status')}, "
                             f"ate {meal.get('grams_eaten')} of {meal.get('grams_dispensed')} g")
        return dog, facts

    @app.post("/chat")
    def chat(body: ChatRequest):
        """Ask Kibbly about one dog, grounded in its facts. Needs a running model (Ollama by default);
        if the model is unreachable the answer is a plain fallback, never an error."""
        dog, facts = resolve_dog(body)
        answer = chat_module.ask(provider_factory(), dog, body.question, facts)
        return {"dog": dog.get("name"), **answer}

    @app.post("/chat/stream")
    def chat_stream(body: ChatRequest):
        """Same as /chat, but streams the answer as plain text while the model writes it, so a slow
        local model shows words within a second or two instead of one long wait."""
        dog, facts = resolve_dog(body)
        provider = provider_factory()

        def pieces():
            for piece in chat_module.stream(provider, dog, body.question, facts):
                yield piece

        return StreamingResponse(pieces(), media_type="text/plain; charset=utf-8")

    def store_document(collection: str, document: dict) -> dict:
        try:
            doc_id = storage.put(collection, document)
        except ContractError as error:
            raise HTTPException(status_code=422, detail={"collection": collection, "errors": error.errors})
        return {"stored": True, "id": doc_id}

    @app.get("/feeder/config", dependencies=[Depends(require_key)])
    def feeder_config(home_id: str):
        """Everything the feeder needs for a home: the calling order, each dog's meals and voice clip,
        and the recognition thresholds. The ESP32-CAM fetches this at startup and after changes."""
        dogs = sorted(storage.query("dogs", home_id=home_id), key=lambda d: d.get("call_order", 99))
        thresholds = RecognitionSettings()
        return {
            "home_id": home_id,
            "calling_order": [d["dog_id"] for d in dogs],
            "dogs": [{
                "dog_id": d["dog_id"],
                "name": d.get("name"),
                "call_order": d.get("call_order"),
                "voice_clip_url": d.get("media", {}).get("voice_clip_url"),
                "recognition_status": d.get("recognition", {}).get("status"),
                "meals": (storage.get("schedules", d["dog_id"]) or {}).get("meals", []),
            } for d in dogs],
            "thresholds": {"accept_score": thresholds.accept_score, "min_margin": thresholds.min_margin},
        }

    @app.post("/feeder/meals", dependencies=[Depends(require_key)])
    def feeder_meals(document: dict):
        """Store a completed meal with its visits, after it is validated against the contract."""
        return store_document("meals", document)

    @app.post("/feeder/visits", dependencies=[Depends(require_key)])
    def feeder_visits(document: dict):
        """Store a visit seen outside a meal (for example a dog begging between meals)."""
        return store_document("visits", document)

    @app.post("/feeder/alerts", dependencies=[Depends(require_key)])
    def feeder_alerts(document: dict):
        """Store a device alert from the feeder (jam, low tank, power cut)."""
        return store_document("alerts", document)

    return app


app = create_app()

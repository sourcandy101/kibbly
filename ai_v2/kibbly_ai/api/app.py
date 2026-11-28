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

import io

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel

from kibbly_ai import __version__
from kibbly_ai.config import Settings, load_settings
from kibbly_ai.engines import decide
from kibbly_ai.storage import Storage, make_storage


class LiveRequest(BaseModel):
    camera_ip: str
    frames: int = 2
    gap: float = 0.3
    flash: bool = False
    meal_dog: str | None = None
    dog_ids: list[str] | None = None


def _split_ids(dog_ids: str | None) -> list | None:
    if not dog_ids:
        return None
    return [d.strip() for d in dog_ids.split(",") if d.strip()]


def _default_camera(ip, frames, gap, flash):
    from kibbly_ai.perception import camera

    return camera.fetch_frames(ip, frames=frames, gap=gap, flash=flash)


def create_app(settings: Settings = None, storage: Storage = None,
               recognizer_provider=None, camera=None) -> FastAPI:
    """recognizer_provider: callable() -> Recognizer, built lazily on first use (real models are heavy).
    camera: callable(ip, frames, gap, flash) -> (images, seconds). Both are injected in tests."""
    settings = settings or load_settings()
    storage = storage or make_storage(settings)
    if recognizer_provider is None:
        from kibbly_ai.perception.pipeline import load_names, load_recognizer

        def recognizer_provider():
            return load_recognizer(settings)

        names_loader = lambda: load_names(settings.gallery_dir)  # noqa: E731
    else:
        names_loader = lambda: {}  # noqa: E731
    camera = camera or _default_camera

    app = FastAPI(title="Kibbly AI server", version=__version__)
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

    return app


app = create_app()

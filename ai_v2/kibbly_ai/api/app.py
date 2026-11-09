"""FastAPI application. Run on the demo laptop:

  .venv\\Scripts\\python.exe -m uvicorn kibbly_ai.api.app:app --host 0.0.0.0 --port 8000

Interactive docs: http://localhost:8000/docs
Endpoints are added step by step; the full list is in ai_v2/architecture.md.
"""

from fastapi import FastAPI

from kibbly_ai import __version__
from kibbly_ai.config import Settings, load_settings
from kibbly_ai.storage import Storage, make_storage


def create_app(settings: Settings = None, storage: Storage = None) -> FastAPI:
    settings = settings or load_settings()
    storage = storage or make_storage(settings)

    app = FastAPI(title="Kibbly AI server", version=__version__)
    app.state.settings = settings
    app.state.storage = storage

    @app.get("/health")
    def health():
        """Liveness check for the feeder, the app and the demo."""
        return {"status": "ok", "version": __version__, "storage": storage.name,
                "llm": f"{settings.llm}:{settings.model}"}

    return app


app = create_app()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router as api_router
from app.tasks import create_start_app_handler


def get_application():
    app = FastAPI(title="Bill Analitics", version="0.0.1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_event_handler("startup", create_start_app_handler(app))

    app.include_router(api_router, prefix="/api")

    return app


app = get_application()

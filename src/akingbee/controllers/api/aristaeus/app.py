from fastapi import FastAPI

from .resources.swarm import router as swarm_router
from .resources.monitoring import router as monitoring_router
from .middlewares.cors import configure_cors_middleware


def create_app():
    app = FastAPI()

    app.include_router(monitoring_router)
    app.include_router(swarm_router, prefix="/swarm")

    configure_cors_middleware(
        app=app,
        allow_origin_regex=r"^https?://(.*\.)?((akingbee\.(com|test))|localhost)(:\d+)?$",
        allow_credentials=True,
    )

    return app

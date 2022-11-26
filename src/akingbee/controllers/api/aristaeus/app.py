from fastapi import FastAPI

import akingbee.infrastructure.db.repositories


from .resources.swarm import router as swarm_router
from .resources.apiary import router as apiary_router
from .resources.hive import router as hive_router
from .resources.monitoring import router as monitoring_router
from .middlewares.cors import configure_cors_middleware

from fastapi.responses import JSONResponse
from fastapi import Request

from akingbee.domains.aristaeus.errors import EntityNotFound


def configure_error_handlers(app):
    @app.exception_handler(EntityNotFound)
    async def entity_not_found_exception_handler(request: Request, exc: EntityNotFound):
        return JSONResponse(
            status_code=404,
            content={"message": "Not Found"},
        )


def create_app():
    app = FastAPI()

    app.include_router(monitoring_router)
    app.include_router(swarm_router, prefix="/swarm")
    app.include_router(apiary_router, prefix="/apiary")
    app.include_router(hive_router, prefix="/hive")
    configure_error_handlers(app)

    configure_cors_middleware(
        app=app,
        allow_origin_regex=r"^https?://(.*\.)?((akingbee\.(com|test))|localhost)(:\d+)?$",
        allow_credentials=True,
    )

    return app

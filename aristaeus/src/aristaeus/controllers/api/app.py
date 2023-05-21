from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from aristaeus.config import settings
from aristaeus.dispatcher import Dispatcher
from aristaeus.domain.errors import BaseException
from aristaeus.domain.errors import EntityNotFound

from .middlewares.cors import configure_cors_middleware
from .resources.apiary import router as apiary_router
from .resources.comment import router as comment_router
from .resources.event import router as event_router
from .resources.hive import router as hive_router
from .resources.monitoring import router as monitoring_router
from .resources.parameter import router as parameter_router
from .resources.swarm import router as swarm_router


def configure_error_handlers(app):
    @app.exception_handler(EntityNotFound)
    async def entity_not_found_exception_handler(request: Request, exc: EntityNotFound):
        return JSONResponse(
            status_code=404,
            content={"message": "Not Found ohoh"},
        )

    @app.exception_handler(BaseException)
    async def base_exception_handler(request: Request, exc: BaseException):
        return JSONResponse(
            status_code=400,
            content={"message": exc.message, "type": exc.__class__.__name__},
        )


def create_app():
    app = FastAPI()

    app.include_router(monitoring_router)
    app.include_router(swarm_router, prefix="/swarm")
    app.include_router(apiary_router, prefix="/apiary")
    app.include_router(hive_router, prefix="/hive")
    app.include_router(event_router, prefix="/event")
    app.include_router(comment_router, prefix="/comment")
    app.include_router(parameter_router, prefix="/parameter")

    configure_error_handlers(app)

    if settings.get("DISABLE_CORS", False):
        origin_regex = r"^https?://.*$"
    else:
        origin_regex = r"^https?://(.*\.)?((aristaeus\.(com|test))|localhost)(:\d+)?$"

    configure_cors_middleware(
        app=app,
        allow_origin_regex=origin_regex,
        allow_credentials=True,
    )

    Dispatcher.init()
    return app

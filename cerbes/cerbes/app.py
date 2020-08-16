from meltingpot.webapp import meltapp, MiddleWare

from .views import router


def create_app():
    app = meltapp()
    app.middleware("http")(MiddleWare(db_enabled=True))
    app.include_router(router)
    return app

app = create_app()

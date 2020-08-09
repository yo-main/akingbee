import fastapi

from .views import router

def create_app():
    app = fastapi.FastAPI()
    app.include_router(router)
    return app


app = create_app()






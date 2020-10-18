from gaea.webapp import AppClient, MiddleWare
from gaea.database import db

from cerbes.views import router


def create_app():
    middleware = MiddleWare(db_client=db())
    client = AppClient(routers=router, middleware=middleware)
    client.add_cors_middleware(allow_origins=["http://localhost:3000"], allow_credentials=True)
    return client.get_app()


app = create_app()

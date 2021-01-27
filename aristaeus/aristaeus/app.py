from gaea.webapp import AppClient, MiddleWare
from gaea.database import db

from aristaeus.api.v1 import ROUTERS


def create_app():
    routers = ROUTERS
    middleware = MiddleWare(db_client=db())
    client = AppClient(routers=routers, middleware=middleware)
    client.add_cors_middleware(
        allow_origins=["http://localhost:3000"], allow_credentials=True
    )
    return client.get_app()


app = create_app()

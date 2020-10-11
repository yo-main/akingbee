from gaea.webapp import AppClient, MiddleWare
from gaea.database import db

from aristaeus.api.v1 import router_apiary, router_setup


def create_app():
    routers = (router_apiary, router_setup)
    middleware = MiddleWare(db_client=db())
    client = AppClient(router=routers, middleware=middleware)
    client.add_cors_middleware(allow_credentials=True)
    return client.get_app()


app = create_app()
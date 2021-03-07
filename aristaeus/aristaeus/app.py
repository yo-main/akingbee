from gaea.webapp import AppClient, MiddleWare
from gaea.database import db

from aristaeus.api.v1 import ROUTERS


def create_app():
    routers = ROUTERS
    middleware = MiddleWare(db_client=db())
    client = AppClient(routers=routers, middleware=middleware)
    client.add_cors_middleware(
        allow_origin_regex=r"^https?://(.*\.)?((akingbee\.(com|test))|localhost)(:\d+)?$",
        allow_credentials=True,
    )
    return client.get_app()


app = create_app()

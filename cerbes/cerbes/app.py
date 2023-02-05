from gaea.database import db
from gaea.webapp import AppClient, MiddleWare

from cerbes.views import router


def create_app():
    middleware = MiddleWare(db_client=db())
    client = AppClient(routers=router, middleware=middleware)
    client.add_cors_middleware(
        # allow_origin_regex=r"^https?://(.*\.)?((akingbee\.(com|test))|localhost)(:\d+)?$",
        allow_credentials=True,
    )
    return client.get_app()


app = create_app()

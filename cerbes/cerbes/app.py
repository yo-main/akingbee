from gaea.database import db
from gaea.webapp import AppClient, MiddleWare
from gaea.config import CONFIG

from cerbes.views import router


def create_app():
    middleware = MiddleWare(db_client=db())
    client = AppClient(routers=router, middleware=middleware)

    if not CONFIG.get("DISABLE_CORS", False):
        client.add_cors_middleware(
            allow_origin_regex=r"^https?://(.*\.)?((akingbee\.(com|test))|localhost)(:\d+)?$",
            allow_credentials=True,
        )

    return client.get_app()


app = create_app()

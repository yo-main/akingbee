from gaea.webapp import AppClient, MiddleWare
from gaea.database import db

from cerbes.views import router


def create_app():
    middleware = MiddleWare(db_client=db())
    client = AppClient(routers=router, middleware=middleware)
    client.add_cors_middleware(
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:8080",
            "http://akingbee.local",
            "http://akingbee.com",
        ],
        allow_credentials=True,
    )
    return client.get_app()


app = create_app()

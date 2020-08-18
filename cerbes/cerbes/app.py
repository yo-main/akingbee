from meltingpot.webapp import meltapp, MiddleWare
from meltingpot.database import db

from .views import router


class AppClient:
    def __init__(self):
        self.app = meltapp()
        self.app.include_router(router)
        self.db_client = None

    def enable_db(self, url=None):
        self.db_client = db(url)

    def _add_middleware(self):
        self.app.middleware("http")(MiddleWare(db_client=self.db_client))

    def get_app(self):
        self._add_middleware()
        return self.app


client = AppClient()
client.enable_db()
app = client.get_app()

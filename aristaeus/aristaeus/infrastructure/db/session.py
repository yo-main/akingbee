from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from aristaeus.domain.adapters.session import SessionManagerAdapter
from aristaeus.infrastructure.db.utils import get_database_uri
from aristaeus.injector import Injector


class FakeSession:
    def __init__(self):
        self.committed = False
        self.rollbacked = False

    async def commit(self, *args, **kwargs):
        self.committed = True

    async def rollback(self, *args, **kwargs):
        self.rollbacked = True

    async def execute(self, *args, **kwargs):
        return None

    def expunge_all(self, *args, **kwargs):
        return None


@Injector.bind(SessionManagerAdapter, "test")
class FakeSessionManager:
    def get(self):
        return FakeSession()


@Injector.bind(SessionManagerAdapter)
class SQLAlchemySessionManager:
    def __init__(self):
        self.engine = create_async_engine(get_database_uri())
        self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    def get(self):
        return self.session_maker()

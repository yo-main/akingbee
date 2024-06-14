from aristaeus.injector import Injector
from aristaeus.injector import InjectorMixin

from aristaeus.domain.adapters.repositories.apiary import ApiaryRepositoryAdapter
from aristaeus.domain.adapters.repositories.comment import CommentRepositoryAdapter
from aristaeus.domain.adapters.repositories.event import EventRepositoryAdapter
from aristaeus.domain.adapters.repositories.hive import HiveRepositoryAdapter
from aristaeus.domain.adapters.repositories.parameter import ParameterRepositoryAdapter
from aristaeus.domain.adapters.repositories.swarm import SwarmRepositoryAdapter
from aristaeus.domain.adapters.repositories.user import UserRepositoryAdapter
from aristaeus.domain.adapters.repositories.harvest import HarvestRepositoryAdapter
from aristaeus.domain.adapters.session import SessionManagerAdapter


class UnitOfWork(InjectorMixin):
    session_manager: SessionManagerAdapter

    async def __aenter__(self):
        self.session = self.session_manager.get()

        self.hive = Injector.get(HiveRepositoryAdapter, kwargs={"session": self.session})
        self.apiary = Injector.get(ApiaryRepositoryAdapter, kwargs={"session": self.session})
        self.swarm = Injector.get(SwarmRepositoryAdapter, kwargs={"session": self.session})
        self.comment = Injector.get(CommentRepositoryAdapter, kwargs={"session": self.session})
        self.event = Injector.get(EventRepositoryAdapter, kwargs={"session": self.session})
        self.parameter = Injector.get(ParameterRepositoryAdapter, kwargs={"session": self.session})
        self.user = Injector.get(UserRepositoryAdapter, kwargs={"session": self.session})
        self.harvest = Injector.get(HarvestRepositoryAdapter, kwargs={"session": self.session})

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.session.expunge_all()  # ensure object can still be accessed after the session is closed
        await self.rollback()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

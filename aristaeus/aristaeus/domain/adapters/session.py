from typing import Protocol


class SessionManagerAdapter(Protocol):
    async def get(self):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...

    async def close(self):
        ...

    async def execute(self, *args, **kwargs):
        ...

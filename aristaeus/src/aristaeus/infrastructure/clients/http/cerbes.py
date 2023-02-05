from typing import Protocol

import aiohttp

from aristaeus.config import settings
from aristaeus.injector import Injector
from aristaeus.utils.singleton import SingletonMeta


class CerbesClientAsyncAdapter(Protocol):
    async def validate(self, access_token: str) -> str | None:
        ...


@Injector.bind(CerbesClientAsyncAdapter, "test")
class TestClient(metaclass=SingletonMeta):
    async def validate(self, access_token: str) -> str | None:
        return access_token


@Injector.bind(CerbesClientAsyncAdapter)
class HttpClient(metaclass=SingletonMeta):
    def __init__(self):
        self.base_url = f"{settings.CERBES_API_ENDPOINT}:{settings.CERBES_API_PORT}"
        if not self.base_url.startswith("http"):
            self.base_url = f"http://{self.base_url}"

    async def validate(self, access_token: str) -> str | None:
        url = f"{self.base_url}/check"

        async with aiohttp.ClientSession() as session:  # TODO: define the session in the __init__ - or better - a base class
            async with session.get(url, cookies={"access_token": access_token}) as resp:
                data = await resp.json()
                return data.get("user_id") if resp.status == 200 else None

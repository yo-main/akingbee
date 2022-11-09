from uuid import UUID

from fastapi import HTTPException
from fastapi import Depends
from fastapi import Cookie

import aiohttp

from akingbee.config import settings

CERBES_URL = f"{settings.CERBES_API_ENDPOINT}:{settings.CERBES_API_PORT}"
if not CERBES_URL.startswith("http"):
    CERBES_URL = f"http://{CERBES_URL}"


async def validate_access_token(access_token):
    url = f"{CERBES_URL}/check"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, cookies={"access_token": access_token}) as resp:
            return await resp.json() if resp.status == 200 else None


async def get_logged_in_user(access_token=Cookie(None)) -> UUID:
    if not access_token:
        raise HTTPException(status_code=401)

    data = await validate_access_token(access_token=access_token)

    if data is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    return UUID(data["user_id"])

from functools import wraps
import uuid

from fastapi import Cookie, HTTPException
import aiohttp

from gaea.config import CONFIG


CERBES_URL = f"{CONFIG.CERBES_API_ENDPOINT}:{CONFIG.CERBES_API_PORT}"


async def validate_access_token(access_token):
    url = f"{CERBES_URL}/check"
    if not url.startswith("http"):
        url = f"http://{url}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, cookies={"access_token": access_token}) as resp:
            return await resp.json() if resp.status == 200 else None


async def get_logged_in_user(access_token):
    if not access_token:
        raise HTTPException(status_code=401)

    data = await validate_access_token(access_token=access_token)

    if data is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    return uuid.UUID(data["user_id"])

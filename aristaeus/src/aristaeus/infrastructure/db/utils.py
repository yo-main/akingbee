import functools

from sqlalchemy.exc import NoResultFound

from aristaeus.config import settings
from aristaeus.domain.errors import EntityNotFound


def get_database_uri(dbname: str | None = None) -> str:
    return "postgresql+asyncpg://{user}:{pwd}@{host}:{port}/{dbname}".format(
        user=settings.database_user,
        pwd=settings.database_password,
        host=settings.database_host,
        port=settings.database_port,
        dbname=dbname or settings.database_dbname,
    )


def error_handler(mapping: dict | None = None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except NoResultFound as exc:
                raise EntityNotFound("Entity not found in database") from exc
            except Exception as exc:
                if mapping and type(exc) in mapping:
                    raise mapping[type(exc)] from exc
                raise

        return wrapper

    return decorator

import fastapi

from meltingpot.database import db


class MiddleWare:
    def __init__(self, db_enabled=False):
        self.db_enabled = db_enabled

    async def before_request(self, *args, **kwargs):
        pass

    async def after_request(self, *args, **kwargs):
        pass

    async def exception_handler(self, *args, **kwargs):
        pass

    async def __call__(self, request: fastapi.Request, call_next):
        await self.before_request()

        if self.db_enabled:
            db.init()

        try:
            response = await call_next(request)

        except:
            await self.exception_handler()
            raise

        finally:

            if self.db_enabled:
                connection = db.session.connection()
                if connection.in_transaction():
                    db.session.rollback()

            await self.after_request()

        return response

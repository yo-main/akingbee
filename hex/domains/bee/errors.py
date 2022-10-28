class BaseException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class EntityPersistError(BaseException):
    pass


class EntityNotFound(BaseException):
    pass


class OwnershipError(BaseException):
    pass

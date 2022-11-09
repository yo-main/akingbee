class BaseException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class EntitySavingError(BaseException):
    pass


class EntityNotFound(BaseException):
    pass

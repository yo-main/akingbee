class BaseException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class EntitySavingError(BaseException):
    pass


class EntityNotFound(BaseException):
    pass


class PermissionError(BaseException):
    pass


class ApiaryCannotBeRemovedSwarmExists(BaseException):
    pass


class CantAttachSwarmOneAlreadyExists(BaseException):
    pass


class CantAttachSwarmNoApiary(BaseException):
    pass

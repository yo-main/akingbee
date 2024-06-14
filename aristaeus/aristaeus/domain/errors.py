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


class ApiaryCannotBeDeletedHiveExists(BaseException):
    pass


class ApiaryCouldNotBeDeleted(BaseException):
    pass


class CantAttachSwarmOneAlreadyExists(BaseException):
    pass


class CantAttachSwarmNoApiary(BaseException):
    pass


class CantHarvestIfNoApiary(BaseException):
    pass


class CantHarvestIfNoSwarm(BaseException):
    pass


class CantHarvestNegativeQuantity(BaseException):
    pass

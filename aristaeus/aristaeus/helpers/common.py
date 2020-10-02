import uuid


def validate_uuid(string):
    try:
        uuid.UUID(string)
        return True
    except:  # pylint: disable=bare-except
        return False

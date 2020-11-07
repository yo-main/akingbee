import uuid


def validate_uuid(value):
    string = str(value)
    try:
        uuid.UUID(string)
        return True
    except:  # pylint: disable=bare-except
        return False

import datetime

from src.errors import errors


def jinja_date_formatting(value, length="short"):
    """
    Used as a jinja filter to print date
    """
    if length == "full":
        return value.strftime("%d/%m/%Y %H:%M:%S")
    else:
        return value.strftime("%d/%m/%Y")


def convert_to_date_object(arg):
    """
    Convert from string to datetime the date value received from the frontend
    """
    if not arg:
        return None

    try:
        date = datetime.datetime.strptime(arg, "%d/%m/%Y")
    except ValueError:
        raise errors.NotDateFormat()

    return date

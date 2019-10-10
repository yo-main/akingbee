import datetime

from src.constants import alert_codes as alerts
from src.services.alerts import Error


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
    if arg == "":
        return ""

    try:
        date = datetime.datetime.strptime(arg, "%d/%m/%Y")
    except ValueError:
        raise Error(alerts.STRING_CANNOT_BE_CONVERTED_TO_DATE)

    return date

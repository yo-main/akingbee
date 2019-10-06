import datetime


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

    args = list(map(int, arg.split("/")))

    day = args[0]
    month = args[1]
    year = args[2]

    myDate = datetime.datetime(year, month, day)

    return myDate

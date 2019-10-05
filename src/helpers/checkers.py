import re


def validate_email(string):
    pattern = re.compile(
        r"^[a-z0-9\._%+-]+@[a-z0-9\.-]+\.[a-z]{2,3}$"
    )
    return bool(pattern.match(string))


def validate_password(string):
    pattern = re.compile(
        r"^(?=.*[a-z])(?=.*[0-9])[a-zA-Z0-9_!@*%&$-]{8,}$"
    )
    return bool(pattern.match(string))

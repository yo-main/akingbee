import pytest
import datetime

from webapp.constants import alert_codes
from webapp.helpers.date import convert_to_date_object, jinja_date_formatting
from webapp.errors import errors


@pytest.mark.parametrize("date", ["12", "12/01", "12/15/19"])
def test_convert_date_fail(date):
    with pytest.raises(errors.NotDateFormat):  # it's ugly - to refacto
        convert_to_date_object(date)


def test_convert_date_success():
    res = convert_to_date_object("01/05/2019")
    assert datetime.datetime(year=2019, month=5, day=1) == res


def test_jinja_date_formatting_short():
    date = datetime.datetime(year=2019, month=5, day=1)
    res = jinja_date_formatting(date)
    assert res == "01/05/2019"


def test_jinja_date_formatting_long():
    date = datetime.datetime(
        year=2019, month=5, day=1, hour=4, minute=3, second=54
    )
    res = jinja_date_formatting(date, length="full")
    assert res == "01/05/2019 04:03:54"

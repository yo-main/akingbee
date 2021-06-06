import datetime
import pytest
import uuid

from gaea.rbmq import RBMQPublisher
from gaea.rbmq.utils.tests import MockRBMQConnectionManager
from gaea.models.utils.test import IDS


def test_get_comments(auth_token, test_app):
    response = test_app.get(f"/comments?hive={IDS['Hives'][0]}")
    assert response.status_code == 401

    response = test_app.get(
        f"/comments?hive_id={IDS['Hives'][0]}", cookies={"access_token": auth_token}
    )
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = test_app.get(
        f"/comments?hive_id={IDS['Hives'][1]}", cookies={"access_token": auth_token}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = test_app.get(
        f"/comments?hive_id={IDS['Hives'][2]}", cookies={"access_token": auth_token}
    )
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = test_app.get(
        f"/comments?hive_id={IDS['Hives'][3]}", cookies={"access_token": auth_token}
    )
    assert response.status_code == 404


@pytest.mark.parametrize(
    "date, event_id, expected",
    (
        ("2020-12-20T01:02:03.012345", None, 200),
        ("2020-12-20T01:02:03012345", None, 422),
        ("2020-12-20T01:02:03.012345", IDS["Events"][0], 200),
        ("2020-12-20T01:02:03.012345", IDS["Events"][-1], 400),
        ("2020-12-20T01:02:03.012345", uuid.uuid4(), 400),
    ),
)
def test_create_comments(auth_token, test_app, date, event_id, expected):
    data = {"comment": "123", "date": date, "event_id": event_id}
    data = {k: str(v) for k, v in data.items() if v is not None}
    response = test_app.post(
        f"/comments/hive/{str(IDS['Hives'][0])}",
        json=data,
        cookies={"access_token": auth_token},
    )
    assert response.status_code == expected

    if expected == 200:
        data = response.json()
        assert (
            data["date"]
            == datetime.datetime(
                year=2020,
                month=12,
                day=20,
                hour=1,
                minute=2,
                second=3,
                microsecond=12345,
            ).isoformat()
        )
        assert data["comment"] == "123"
        assert data["type"] == "user"

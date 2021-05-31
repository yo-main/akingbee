import datetime
import pytest
import uuid

from gaea.rbmq import RBMQPublisher
from gaea.rbmq.utils.tests import MockRBMQConnectionManager
from gaea.models.utils.test import IDS


def test_get_events(auth_token, test_app):
    response = test_app.get("/events")
    assert response.status_code == 401

    response = test_app.get("/events", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_single_event(auth_token, test_app):
    response = test_app.get(f"/events/{IDS['Events'][0]}")
    assert response.status_code == 401

    response = test_app.get(
        f"/events/{IDS['Events'][0]}", cookies={"access_token": auth_token}
    )
    assert response.status_code == 200

    response = test_app.get(
        f"/events/{IDS['Events'][1]}", cookies={"access_token": auth_token}
    )
    assert response.status_code == 200

    response = test_app.get(
        f"/events/{IDS['Events'][-1]}", cookies={"access_token": auth_token}
    )
    assert response.status_code == 404


@pytest.mark.parametrize(
    "due_date, status_id, type_id, hive_id, expected",
    (
        (
            "2020-12-20T01:02:03.012345",
            IDS["Event_statuses"][0],
            IDS["Event_types"][0],
            None,
            200,
        ),
        (
            "2020-12-20T01:02:03.012345",
            IDS["Event_statuses"][1],
            IDS["Event_types"][0],
            None,
            200,
        ),
        (
            "2020-12-20T01:02:03.012345",
            IDS["Event_statuses"][0],
            IDS["Event_types"][1],
            None,
            200,
        ),
        (
            "2020-12-20T01:02:03.012345",
            IDS["Event_statuses"][0],
            IDS["Event_types"][-1],
            None,
            400,
        ),
        (
            "2020-12-20T01:02:03.012345",
            IDS["Event_statuses"][-1],
            IDS["Event_types"][0],
            None,
            400,
        ),
        (
            "2020-12-20T01:02:03.012345",
            IDS["Event_statuses"][0],
            IDS["Event_types"][0],
            IDS["Hives"][0],
            200,
        ),
        (
            "2020-12-20T01:02:03.012345",
            IDS["Event_statuses"][0],
            IDS["Event_types"][0],
            IDS["Hives"][-1],
            404,
        ),
    ),
)
def test_create_events(
    auth_token, test_app, due_date, status_id, type_id, hive_id, expected
):
    data = {
        "title": "title",
        "description": "desc",
        "due_date": due_date,
        "hive_id": hive_id,
        "status_id": status_id,
        "type_id": type_id,
    }
    data = {k: str(v) for k, v in data.items() if v is not None}

    response = test_app.post(
        "/events",
        json=data,
        cookies={"access_token": auth_token},
    )
    assert response.status_code == expected

    if expected == 200:
        data = response.json()
        assert (
            data["due_date"]
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


def test_delete_events(auth_token, test_app):
    data = {
        "title": "title",
        "description": "description",
        "due_date": "2020-12-20T01:02:03.012345",
        "status_id": str(IDS["Event_statuses"][0]),
        "type_id": str(IDS["Event_types"][0]),
        "hive_id": str(IDS["Hives"][0]),
    }

    response = test_app.post(
        "/events",
        json=data,
        cookies={"access_token": auth_token},
    )
    assert response.status_code == 200

    event_id = response.json()["id"]

    response = test_app.get(f"/events/{event_id}", cookies={"access_token": auth_token})
    assert response.status_code == 200

    response = test_app.delete(
        f"/events/{event_id}", cookies={"access_token": auth_token}
    )
    assert response.status_code == 204

    response = test_app.get(f"/events/{event_id}", cookies={"access_token": auth_token})
    assert response.status_code == 404

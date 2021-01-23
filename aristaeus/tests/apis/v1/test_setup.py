import pytest

from gaea.rbmq import RBMQPublisher
from gaea.rbmq.utils.tests import MockRBMQConnectionManager

from aristaeus.api.v1.views.setup import MAPPING

@pytest.mark.parametrize("data_type", MAPPING.keys())
def test_get_data(auth_token, test_app, data_type):
    response = test_app.get(f"/setup/{data_type}", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.parametrize("data_type", MAPPING.keys())
def test_post_data(auth_token, test_app, data_type):
    response = test_app.post(f"/setup/{data_type}", cookies={"access_token": auth_token}, json={"value": "coucou"})
    assert response.status_code == 200
    assert response.json().get("id")

    response = test_app.get(f"/setup/{data_type}", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 3

@pytest.mark.parametrize("data_type", MAPPING.keys())
def test_update_data(auth_token, test_app, data_type):
    response = test_app.get(f"/setup/{data_type}", cookies={"access_token": auth_token})
    assert response.status_code == 200

    data = response.json()
    obj = next((o for o in data if o["name"] == "coucou"), None)
    assert obj

    response = test_app.put(f"/setup/{data_type}/{obj['id']}", cookies={"access_token": auth_token}, json={"value": "oucouc"})
    assert response.status_code == 204

@pytest.mark.parametrize("data_type", MAPPING.keys())
def test_delete_data(auth_token, test_app, data_type):
    response = test_app.get(f"/setup/{data_type}", cookies={"access_token": auth_token})
    assert response.status_code == 200

    data = response.json()
    obj = next((o for o in data if o["name"] == "oucouc"), None)
    assert obj

    response = test_app.delete(f"/setup/{data_type}/{obj['id']}", cookies={"access_token": auth_token})
    assert response.status_code == 204

    response = test_app.get(f"/setup/{data_type}", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 2


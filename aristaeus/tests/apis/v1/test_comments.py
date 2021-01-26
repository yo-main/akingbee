import pytest
import uuid

from gaea.rbmq import RBMQPublisher
from gaea.rbmq.utils.tests import MockRBMQConnectionManager
from gaea.models.utils.test import IDS

def test_get_comments(auth_token, test_app):
    response = test_app.get(f"/hive/{IDS['Hives'][0]}/comments")
    assert response.status_code == 401

    response = test_app.get(f"/hive/{IDS['Hives'][0]}/comments", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = test_app.get(f"/hive/{IDS['Hives'][1]}/comments", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = test_app.get(f"/hive/{IDS['Hives'][2]}/comments", cookies={"access_token": auth_token})
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = test_app.get(f"/hive/{IDS['Hives'][3]}/comments", cookies={"access_token": auth_token})
    assert response.status_code == 404


from fastapi.testclient import TestClient
from akingbee.controllers.aristaeus.api.app import create_app


def test_unlog_user():
    client = TestClient(app=create_app())
    response = client.post("/swarm")
    assert response.status_code == 401, response.text

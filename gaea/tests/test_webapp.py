from fastapi.testclient import TestClient

from gaea.webapp import AppClient


def test_webapp():
    app = AppClient(routers=[])
    test_client = TestClient(app.get_app())

    response = test_client.get("/_/status")
    assert response.status_code == 200

    response = test_client.get("/status")
    assert response.status_code == 404

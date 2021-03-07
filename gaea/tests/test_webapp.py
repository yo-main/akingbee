from fastapi.testclient import TestClient
from fastapi import APIRouter

from gaea.webapp import AppClient, MiddleWare


router = APIRouter()


@router.get("/test_error", status_code=204)
def error():
    raise Exception()
    return ""


def test_webapp():
    app = AppClient(routers=[router], middleware=MiddleWare())
    test_client = TestClient(app.get_app())

    response = test_client.get("/_/status")
    assert response.status_code == 200

    response = test_client.get("/status")
    assert response.status_code == 404

    response = test_client.get("/test_error")
    assert response.status_code == 500

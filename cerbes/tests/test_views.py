# pylint: disable=redefined-outer-name,unused-import
import base64
import jwt
import uuid

import pytest

from gaea.rbmq import RBMQPublisher
from gaea.rbmq.utils.tests import MockRBMQConnectionManager

from cerbes.helpers import generate_jwt


@pytest.mark.parametrize(
    "username, password, email, expected_code, expected_msg",
    (
        ("Maya", "ILoveYouHoney1", "maya.labeille@akingbee.com", 200, None),
        ("coucou", "coucou", "coucou", 400, "Invalid email address"),
        ("coucou", "coucou", "coucou@cou", 400, "Invalid email address"),
        ("coucou", "coucou", "@cou.com", 400, "Invalid email address"),
        ("coucou", "coucou", "coucou@.c", 400, "Invalid email address"),
        ("coucou", "coucou", "coucou@coucou.com", 400, "Invalid password"),
        ("coucou", "coucou1", "coucou@coucou.com", 400, "Invalid password"),
        ("coucou", "c!ucAZEd", "coucou@coucou.com", 400, "Invalid password"),
        ("coucou", "c!uAad&é1", "coucou@coucou.com", 200, None),
        ("doudou", "d!udoudou1", "coucou@coucou.com", 400, "Email already exists"),
        ("coucou", "d!udoudou1", "doudou@doudou.com", 400, "Username already exists"),
    ),
)
def test_register_user(
    test_app, username, password, email, expected_code, expected_msg, mock_rbmq_channel
):
    data = {"username": username, "password": password, "email": email}
    response = test_app.post("/user", json=data, cookies={"language": "en"})
    assert response.status_code == expected_code
    content = response.json()
    assert expected_msg == (content["detail"] if expected_code != 200 else None)
    assert mock_rbmq_channel.basic_publish.call_count == (
        1 if expected_code == 200 else 0
    )


@pytest.mark.parametrize(
    "creds,expected_code,expected_content",
    (
        (None, 401, "Missing authorization header"),
        ("testtest", 401, "Could not parse access_token"),
        ("::testtest", 401, "Could not parse access_token"),
        ("te:s:ttest", 401, "Could not parse access_token"),
        (":testtest", 401, "Wrong credentials"),
        ("testtest:", 401, "Wrong credentials"),
        ("Maya:ILovehoney", 401, "Wrong credentials"),
        ("ILoveHoney:Maya", 401, "Wrong credentials"),
        ("maya:ilovehoney", 401, "Wrong credentials"),
        ("maya.labeille@akingbee.com:ILoveHoney", 401, "Wrong credentials"),
        ("Maya:ILoveYouHoney1", 200, None),
    ),
)
def test_login(test_app, creds, expected_code, expected_content):
    headers = {}

    if creds is not None:
        creds = base64.b64encode(creds.encode()).decode()
        headers["Authorization"] = f"Basic {creds}"

    response = test_app.post("/login", headers=headers)
    assert response.status_code == expected_code
    if expected_content:
        assert response.json() == {"detail": expected_content}
    else:
        data = response.json()
        assert jwt.decode(
            data["access_token"],
            options={"verify_signature": False},
            algorithms=["HS256"],
        )
        with pytest.raises(jwt.InvalidSignatureError):
            jwt.decode(data["access_token"], algorithms=["HS256"])


def test_check_jwt(test_app):
    creds = base64.b64encode("Maya:ILoveYouHoney1".encode()).decode()
    response = test_app.post("/login", headers={"Authorization": f"Basic {creds}"})
    jwt = response.json()["access_token"]

    response = test_app.get("/check")
    assert response.status_code == 401

    response = test_app.get("/check", cookies={"access_token": ""})
    assert response.status_code == 401

    response = test_app.get("/check", cookies={"access_token": f"Basic {jwt}"})
    assert response.status_code == 401

    response = test_app.get("/check", cookies={"access_token": jwt})
    assert response.status_code == 200
    assert "user_id" in response.json()


def test_activate_user(test_app, mock_rbmq_channel):
    data = {"username": "hello", "password": "pwd123&éA", "email": "test@test.test"}
    response = test_app.post("/user", json=data, cookies={"language": "en"})

    assert response.status_code == 200

    user = response.json()

    payload = {"user_id": user["id"], "activation_id": user["activation_id"]}

    response = test_app.post(
        "/activate",
        json={"user_id": user["activation_id"], "activation_id": user["id"]},
    )
    assert response.status_code == 404

    response = test_app.post(
        "/activate", json={"user_id": user["id"], "activation_id": str(uuid.uuid4())}
    )
    assert response.status_code == 400

    response = test_app.post("/activate", json=payload)
    assert response.status_code == 201

    response = test_app.post("/activate", json=payload)
    assert response.status_code == 200


def test_reset_user_password(test_app, mock_rbmq_channel):
    data = {
        "username": "forgot",
        "password": "pwd123&éA",
        "email": "forgot@password.test",
    }
    response = test_app.post("/user", json=data, cookies={"language": "en"})
    assert response.status_code == 200

    user = response.json()

    response = test_app.post(
        "/password-reset/request",
        json={"username": "forgot"},
        cookies={"language": "en"},
    )
    assert response.status_code == 201

    reset_id = response.json()["reset_id"]

    response = test_app.get(
        "/password-reset/validate", params={"user_id": user["id"], "reset_id": reset_id}
    )
    assert response.status_code == 200

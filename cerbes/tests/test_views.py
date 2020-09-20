
# pylint: disable=redefined-outer-name,unused-import
import base64
import jwt
import uuid

import pytest

from cerbes.helpers import generate_jwt



@pytest.mark.parametrize("username, password, email, expected_code, expected_msg", (
    ("Maya", "ILoveYouHoney1", "maya.labeille@akingbee.com", 204, None),
    ("coucou", "coucou", "coucou", 400, "Invalid email address"),
    ("coucou", "coucou", "coucou@cou", 400, "Invalid email address"),
    ("coucou", "coucou", "@cou.com", 400, "Invalid email address"),
    ("coucou", "coucou", "coucou@.c", 400, "Invalid email address"),
    ("coucou", "coucou", "coucou@coucou.com", 400, "Invalid password"),
    ("coucou", "coucou1", "coucou@coucou.com", 400, "Invalid password"),
    ("coucou", "c!ucAZEd", "coucou@coucou.com", 400, "Invalid password"),
    ("coucou", "c!uAad&é1", "coucou@coucou.com", 204, None),
    ("doudou", "d!udoudou1", "coucou@coucou.com", 400, "Email already exists"),
    ("coucou", "d!udoudou1", "doudou@doudou.com", 400, "Username already exists"),
))
def test_register_user(test_app, username, password, email, expected_code, expected_msg):
    data = {"username": username, "password": password, "email": email}
    response = test_app.post("/user", json=data)
    assert response.status_code == expected_code
    content = response.json()
    assert expected_msg == (content["detail"] if expected_code != 204 else None)



@pytest.mark.parametrize("creds,expected_code,expected_content", (
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
))
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
        assert jwt.decode(data["access_token"], verify=False, algorithm="HS256")
        with pytest.raises(jwt.InvalidSignatureError):
            jwt.decode(data["access_token"], algorithm="HS256")


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
    assert response.status_code == 204



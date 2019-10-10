import datetime

import pytest
import flask

from src.constants import alert_codes
from src.helpers.helpers import create_new_user
from tests.fixtures import client, fake_database
from src.data_access.pw_objects import User


@pytest.mark.parametrize("name,location,honey_type,status,expected", [
    ("", "Location", "1", "1", alert_codes.MISSING_INFORMATION_APIARY),
    ("Name", "", "1", "1", alert_codes.MISSING_INFORMATION_APIARY),
    ("Name", "Location", "", "1", alert_codes.MISSING_INFORMATION_APIARY),
    ("Name", "Location", "1", "", alert_codes.MISSING_INFORMATION_APIARY),
    ("Name", "Location", "9", "1", alert_codes.INCONSISTANT_DATA),
    ("Name", "Location", "1", "5", alert_codes.INCONSISTANT_DATA),
])
def test_create_apiary_fail(name, location, honey_type, status, expected, client):
    with client.session_transaction() as session:
        session["user_id"] = 1

    data = {
        "name": name,
        "location": location,
        "honey_type": honey_type,
        "status": status,
        "birthday": "01/01/2019",
    }
    answer = client.post("/apiary/create", data=data)
    assert answer.status_code == 500
    assert answer.json["code"] == expected
    

def test_create_apiary_success(client):
    with client.session_transaction() as session:
        session["user_id"] = 1

    data = {
        "name": "apiary",
        "location": "here",
        "honey_type": "1",
        "status": "1",
        "birthday": "01/01/2019",
    }
    answer = client.post("/apiary/create", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.NEW_APIARY_SUCCESS
    
    
def test_create_new_apiary_status_fail(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        
    data = {"name_fr": "test", "name_en": ""}
    answer = client.post("/apiary/create/new_apiary_status", data=data)
    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.INCONSISTANT_DATA
    
    
def test_create_new_apiary_status_success(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        
    data = {"name_fr": "test", "name_en": "te"}
    answer = client.post("/apiary/create/new_apiary_status", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.NEW_PARAMETER_SUCCESS
    

def test_create_new_honey_type_fail(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        
    data = {"name_fr": "test", "name_en": ""}
    answer = client.post("/apiary/create/new_honey_type", data=data)
    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.INCONSISTANT_DATA
    

def test_create_new_honey_type_success(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        
    data = {"name_fr": "test", "name_en": "te"}
    answer = client.post("/apiary/create/new_honey_type", data=data)
    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.NEW_PARAMETER_SUCCESS
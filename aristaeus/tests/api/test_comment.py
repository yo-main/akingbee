import uuid
from datetime import datetime
from datetime import timezone

import pytest
from tests.factories import CommentModelFactory
from tests.factories import HiveModelFactory


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_create_comment(async_app, session):
    hive = HiveModelFactory.build()
    session.add(hive)
    await session.commit()
    await session.refresh(hive)
    data = {
        "body": "body",
        "date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
    }
    response = await async_app.post(f"/comment/{hive.public_id}", json=data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["type"] == "user", data
    assert data["body"] == "body", data
    assert data["date"] == "2022-01-01T00:00:00", data
    assert data["hive_id"] == str(hive.public_id), data


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
@pytest.mark.parametrize(
    "payload",
    (
        {"body": None},
        {"date": None},
        {"date": "i_am_not_a_date"},
    ),
)
async def test_create_comment__wrong_payload(async_app, payload):
    data = {
        "type": "type",
        "body": "description",
        "date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
    }
    data.update(payload)
    data = {k: v for k, v in data.items() if v is not None}
    response = await async_app.post(f"/comment/{uuid.uuid4()}", json=data)
    assert response.status_code == 422, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_comment__unknown(async_app):
    response = await async_app.get(f"/comment/{uuid.uuid4()}")
    assert response.status_code == 404, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_get_comment(async_app, session):
    hive = HiveModelFactory.build()
    session.add(hive)
    await session.commit()
    await session.refresh(hive)

    data = {
        "body": "description",
        "date": datetime(2022, 1, 1, tzinfo=timezone.utc).isoformat(),
    }
    response = await async_app.post(f"/comment/{hive.public_id}", json=data)
    assert response.status_code == 200, response.text

    comment_id = response.json()["public_id"]
    response = await async_app.get(f"/comment/{comment_id}")
    assert response.status_code == 200, response.text


@pytest.mark.parametrize("async_app", ["33333333-3333-3333-3333-333333333333"], indirect=True)
async def test_list_comments(async_app, session):
    hive = HiveModelFactory.build(
        organization_id="33333333-3333-3333-3333-333333333333", public_id="44444444-4444-4444-4444-444444444444"
    )
    session.add(hive)
    await session.commit()
    await session.refresh(hive)
    comments = CommentModelFactory.create_batch(5, hive_id=hive.id)
    session.add_all(comments)
    await session.commit()

    response = await async_app.get("/comment", params={"hive_id": "44444444-4444-4444-4444-444444444444"})

    assert response.status_code == 200, response.text
    assert len(response.json()) == 5, response.text


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
@pytest.mark.parametrize(
    "payload",
    (
        {"body": "new body"},
        {"date": "2022-02-01T00:00:00"},
        {"type": "new type"},
    ),
)
async def test_put_comment__success(async_app, session, payload):
    hive = HiveModelFactory.build(organization_id="11111111-1111-1111-1111-111111111111")
    session.add(hive)
    await session.commit()
    await session.refresh(hive)
    comment = CommentModelFactory.create(hive_id=hive.id)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    data = {"body": "body", "date": "2022-01-01T00:00:00", "type": "type"}

    response = await async_app.put(f"/comment/{comment.public_id}", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in payload.items():
        assert data[key] == value


@pytest.mark.parametrize("async_app", ["11111111-1111-1111-1111-111111111111"], indirect=True)
async def test_delete_hive__success(async_app, session):
    hive = HiveModelFactory.build(organization_id="11111111-1111-1111-1111-111111111111")
    session.add(hive)
    await session.commit()
    await session.refresh(hive)
    comment = CommentModelFactory.create(hive_id=hive.id)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    response = await async_app.delete(f"/comment/{comment.public_id}")
    assert response.status_code == 204, response.text

    response = await async_app.get(f"/comment/{comment.public_id}")
    assert response.status_code == 404, response.text

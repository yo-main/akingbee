from datetime import datetime
from uuid import uuid4

from aristaeus.domain.entities.comment import Comment
from aristaeus.domain.entities.hive import Hive


def test_comment_model():
    now = datetime.now()
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=uuid4())
    comment = Comment(date=now, body="body", type="type", hive=hive)

    assert comment.date == now
    assert comment.body == "body"
    assert comment.type == "type"
    assert comment.hive == hive
    assert comment.public_id is not None


def test_comment_equal():
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=uuid4())
    comment = Comment(date=datetime.now(), body="body", type="type", hive=hive)
    other = Comment(date=datetime.now(), body="body", type="type", hive=hive)
    same = Comment(date=datetime.now(), body="body", type="type", hive=hive, public_id=comment.public_id)

    assert comment != other
    assert comment == same


def test_comment_change_body():
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=uuid4())
    comment = Comment(date=datetime.now(), body="body", type="type", hive=hive)

    comment.change_body("new body")

    assert comment.body == "new body"


def test_comment_change_date():
    hive = Hive(name="name", condition="condition", owner="owner", organization_id=uuid4())
    comment = Comment(date=datetime.now(), body="body", type="type", hive=hive)

    comment.change_date(datetime(2022, 1, 1))

    assert comment.date == datetime(2022, 1, 1)

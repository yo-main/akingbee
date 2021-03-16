import pytest

from gaea.config import CONFIG

from hermes.constants import SENDER, TO
from hermes.email_engine import EmailEngine


@pytest.fixture(scope="module", autouse=True)
def set_config():
    CONFIG.set("COUCOU_EMAIL_PASSWORD", "123")
    CONFIG.set("SENDER_EMAIL_PASSWORD", "LoveYou")
    CONFIG.set("EMAIL_SERVER_HOST", "host")
    CONFIG.set("EMAIL_SERVER_PORT", "1234")

    yield

    CONFIG.unset("COUCOU_EMAIL_PASSWORD", force=True)
    CONFIG.unset("SENDER_EMAIL_PASSWORD", force=True)


class MockMessage:
    email = {SENDER: "sender@test.test", TO: "receiver@test.test"}


def test_email_engine_login(mock_smtp):
    engine = EmailEngine()

    with pytest.raises(ValueError):
        engine.login("unknown_email@c.con")

    engine.login("coucou@cou.cou")
    assert "coucou@cou.cou" in engine.open_connections
    mock_smtp.login.assert_called_once()


def test_email_engine_send(mock_smtp):
    engine = EmailEngine()

    engine.send(MockMessage())
    assert "sender@test.test" in engine.open_connections
    mock_smtp.login.assert_called_once()
    mock_smtp.send_message.assert_called_once()

    engine.close()

    assert "sender@test.test" not in engine.open_connections


def test_email_engine_close(mock_smtp):
    engine = EmailEngine()

    engine.login("coucou@cou.cou")
    engine.login("sender@test.test")

    assert "sender@test.test" in engine.open_connections
    assert "coucou@cou.cou" in engine.open_connections

    engine.close("sender@test.test")

    assert "sender@test.test" not in engine.open_connections
    assert "coucou@cou.cou" in engine.open_connections

    engine.close("carambar@aye.lalala")

    assert "coucou@cou.cou" in engine.open_connections

    engine.close()
    assert "coucou@cou.cou" not in engine.open_connections

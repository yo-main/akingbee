import pytest

from gaea.config import CONFIG

from hermes.constants import SENDER, TO
from hermes.email_engine import EmailEngine


class MockMessage:
    email = {SENDER: "sender@test.test", TO: "receiver@test.test"}


def test_email_engine_login(mock_smtp):
    engine = EmailEngine()

    with pytest.raises(ValueError):
        engine.login("coucou@cou.cou")

    CONFIG.set("COUCOU_EMAIL_PASSWORD", "123")
    engine.login("coucou@cou.cou")
    assert "coucou@cou.cou" in engine.open_connections
    mock_smtp.login.assert_called_once()


def test_email_engine_send(mock_smtp):
    engine = EmailEngine()

    with pytest.raises(ValueError):
        engine.send(MockMessage())

    CONFIG.set("SENDER_EMAIL_PASSWORD", "LoveYou")

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

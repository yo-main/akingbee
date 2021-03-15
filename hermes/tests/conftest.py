import smtplib

import pytest
from mock import Mock, MagicMock

from gaea.rbmq.base import RBMQConnectionManager


@pytest.fixture()
def mock_smtp(monkeypatch):
    client = Mock()
    monkeypatch.setattr(smtplib, "SMTP_SSL", MagicMock(return_value=client))
    return client


@pytest.fixture()
def mock_rbmq_channel(monkeypatch):
    mocked_channel = Mock()
    mocked_conn = Mock()
    monkeypatch.setattr(mocked_conn, "channel", MagicMock(return_value=mocked_channel))
    monkeypatch.setattr(
        RBMQConnectionManager, "_get_connection", MagicMock(return_value=mocked_conn)
    )
    return mocked_channel

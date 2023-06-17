import smtplib

import pytest
from mock import Mock, MagicMock


@pytest.fixture()
def mock_smtp(monkeypatch):
    client = Mock()
    monkeypatch.setattr(smtplib, "SMTP_SSL", MagicMock(return_value=client))
    return client


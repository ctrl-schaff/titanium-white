"""
Tests for exercising titanium-white object construction
for utilizing our exposed API
"""

import os
from loguru import logger
import pytest

from titanium_white import CourtSession


def test_courtlistener_empty_construction(mock_courtlistener_api_key):
    """
    Test generating and using a CourtListener instance with no arguments
    """
    session_instance = CourtSession()
    logger.info(session_instance)

    assert session_instance.api_key == os.environ["COURTLISTENER"]

    os.environ.pop("COURTLISTENER", None)

    with pytest.raises(KeyError):
        session_instance = CourtSession()
        logger.info(session_instance)


def test_courtsession_construction():
    """
    Test generating a CourtSession instance using an API key directly
    """
    os.environ.pop("COURTLISTENER", None)
    mock_api_key = "MOCK_API_KEY"
    session_instance = CourtSession(mock_api_key)

    assert mock_api_key == session_instance.api_key

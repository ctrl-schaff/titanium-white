"""
Tests for exercising titanium-white object construction
for utilizing our exposed API
"""

from loguru import logger
import pytest

from titanium_white import CourtListener, CourtSession


def test_empty_courtlistener_construction():
    """
    Test generating and using a CourtListener instance with no arguments
    """
    with pytest.raises(KeyError):
        listener_instance = CourtListener()
        logger.info(listener_instance)


def test_courtsession_construction(mock_courtlistener_api_key):
    """
    Test generating and using a CourtSession instance
    """
    mock_endpoint = "https://courtlistener.fake/api/rest/v3/mock"
    session_instance = CourtSession(
        endpoint_base=mock_endpoint,
        api_key=mock_courtlistener_api_key,
        headers={},
        parameters={},
    )
    assert session_instance.endpoint_base == mock_endpoint
    assert session_instance.api_key == mock_courtlistener_api_key
    assert not session_instance.headers
    assert not session_instance.parameters
    assert isinstance(session_instance, CourtSession)


def test_courtsession_and_courtlistener(mock_courtlistener_api_key):
    """
    Test generating and using a CourtListener instance constructed
    from a CourtSession
    """
    mock_endpoint = "https://courtlistener.fake/api/rest/v3/mock"
    session_instance = CourtSession(
        endpoint_base=mock_endpoint,
        api_key=mock_courtlistener_api_key,
        headers={},
        parameters={},
    )
    assert session_instance.endpoint_base == mock_endpoint
    assert session_instance.api_key == mock_courtlistener_api_key
    assert not session_instance.headers
    assert not session_instance.parameters
    assert isinstance(session_instance, CourtSession)

    listener_instance = CourtListener(court_session=session_instance)
    assert listener_instance.court_session == session_instance

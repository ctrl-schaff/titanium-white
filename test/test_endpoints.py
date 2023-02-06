"""
Tests for mocking and processing the courtlistener API
endpoints to ensure we properly handle the responses
"""

from loguru import logger
import pytest
import responses

from titanium_white import CourtListener, CourtSession


@responses.activate
def test_people_endpoint_response(
    mock_courtlistener_api_key, people_endpoint_response
) -> None:
    """
    Test endpoint functionality for constructing a request
    and processing the subsequent response
    """
    # https://www.courtlistener.com/api/rest/v3/people/?name_first=Cynthia&name_last=Freeland
    people_endpoint = "https://courtlistener.com/api/rest/v3/people"
    endpoint_parameters = {"name_first": "Cynthia", "name_last": "Freeland"}
    session_instance = CourtSession(
        endpoint=people_endpoint,
        api_key=mock_courtlistener_api_key,
        headers={},
        endpoint_parameters=endpoint_parameters,
    )

    responses.add(responses.GET, people_endpoint, json=people_endpoint_response)

    listener_instance = CourtListener(court_session=session_instance)
    response_object, request_object = listener_instance.get_query()
    assert response_object.json(), people_endpoint_response

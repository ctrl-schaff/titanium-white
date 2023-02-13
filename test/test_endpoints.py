"""
Tests for mocking and processing the courtlistener API
endpoints to ensure we properly handle the responses
"""

from loguru import logger
import responses

from titanium_white import CourtSession


@responses.activate
def test_people_endpoint_response(mock_courtlistener_api_key, people_endpoint_response) -> None:
    """
    Test endpoint functionality for constructing a request
    and processing the subsequent response
    """
    # https://www.courtlistener.com/api/rest/v3/people/?name_first=Cynthia&name_last=Freeland
    session_instance = CourtSession(mock_courtlistener_api_key)

    people_endpoint = "https://courtlistener.com/api/rest/v3/people"
    responses.add(responses.GET, people_endpoint, json=people_endpoint_response)

    endpoint_parameters = {"name_first": "Cynthia", "name_last": "Freeland"}
    response_object, request_object = session_instance.get_query(
        url=people_endpoint, headers={}, params=endpoint_parameters
    )
    logger.info(response_object)
    logger.info(request_object)
    assert response_object.json(), people_endpoint_response


@responses.activate
def test_court_selection(mock_courtlistener_api_key, court_endpoint_response) -> None:
    """
    Filter the courts for the following courts:
        > California Supreme Court
    """
    # https://www.courtlistener.com/api/rest/v3/courts/?full_name=California+Supreme+Court
    court_endpoint = "https://courtlistener.com/api/rest/v3/courts"
    responses.add(responses.GET, court_endpoint, json=court_endpoint_response)
    with CourtSession(mock_courtlistener_api_key) as session_instance:
        court_parameters = {"full_name": "California Supreme Court"}

        response_object, request_object = session_instance.get_query(
            url=court_endpoint, params=court_parameters
        )
        logger.info(response_object)
        logger.info(request_object)

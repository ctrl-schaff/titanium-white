"""
Fixtures for testing titanium-white package
"""

import json
import os
from pathlib import Path
from typing import Union

from loguru import logger
import pytest


@pytest.fixture(scope="session", autouse=True)
def mock_courtlistener_api_key() -> None:
    """
    Sets a mock key value for the courtlistener API key
    """
    courtlistener_env = "COURTLISTENER"
    os.environ[courtlistener_env] = "MOCK_COURTLISTENER_API_KEY"


def load_response(response_path: Union[str, Path]) -> dict:
    """
    Generic method for handling the loading of the JSON
    response data from the endpoint
    """
    try:
        with open(str(response_path), "r", encoding="utf-8") as json_handle:
            response_obj = json.load(json_handle)
    except json.decoder.JSONDecodeError as json_decode_err:
        json_err_msg = f"Unable to load {str(response_path)} internally as JSON object"
        logger.error(json_err_msg)
        raise json_decode_err
    return response_obj


@pytest.fixture(scope="session")
def people_endpoint_response() -> dict:
    """
    Fixture for loading example data from specific endpoints
    from the courtlistener API

    Loads the response produced by hitting the following endpoitn
    https://www.courtlistener.com/api/rest/v3/people/?name_first=Cynthia&name_last=Freeland
    """
    endpoint_path = Path("./test/data/test_people_endpoint_response.json").absolute()
    endpoint_response = load_response(endpoint_path)
    return endpoint_response

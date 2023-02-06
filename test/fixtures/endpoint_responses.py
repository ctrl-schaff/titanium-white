"""
Fixtures for loading example data from specific endpoints
from the courtlistener API
"""

import json
from pathlib import Path
from typing import Union

from loguru import logger
import pytest


def load_response(response_path: Union[str, Path]) -> dict:
    """
    Generic method for handling the loading of the JSON
    response data from the endpoint
    """
    try:
        response_obj = json.loads(str(response_path))
    except json.decoder.JSONDecodeError as json_decode_err:
        json_err_msg = f"Unable to load {str(response_path)} internally as JSON object"
        logger.error(json_err_msg)
        raise json_decode_err(json_err_msg)
    return response_obj


@pytest.fixture(scope="session")
def people_endpoint_response() -> dict:
    """
    Loads the response produced by hitting the following endpoitn
    https://www.courtlistener.com/api/rest/v3/people/?name_first=Cynthia&name_last=Freeland
    """
    endpoint_path = Path("./data/test_people_endpoint_response.json").absolute()
    endpoint_response = load_response(endpoint_path)
    return endpoint_response

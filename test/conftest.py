"""
Fixtures for testing titanium-white package
"""

import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def mock_courtlistener_api_key() -> None:
    """
    Sets a mock key value for the courtlistener API key
    """
    courtlistener_env = "COURTLISTENER"
    os.environ[courtlistener_env] = "MOCK_COURTLISTENER_API_KEY"

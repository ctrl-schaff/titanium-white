"""
Methods for handling the authorization for querying the
courtlistener REST API
"""

import os

from loguru import logger


def load_api_key(courtlistener_env: str = None) -> str:
    """
    Attempts to load the api key from the environment variable
    specified as the "courtlistener_env" argument. If no argument
    is provided then we default to searching for the environment
    variable "COURTLISTENER"
    """
    if courtlistener_env is None:
        courtlistener_env = "COURTLISTENER"

    try:
        api_key = os.environ[courtlistener_env]
    except KeyError as key_err:
        logger.exception(key_err)
        env_error_msg = (
            "Missing COURTLISTENER API token\n"
            "Either set the environment variable or pass"
            "to the <api_key_instance> constructor argument"
        )
        logger.error(env_error_msg)
        raise key_err
    else:
        logger.debug((f"Discovered api key " f"[{courtlistener_env}]={api_key}"))
    return api_key

"""
Collection of classes for implementating the wrapper around
the courtlistener API
"""
import os

from loguru import logger
import requests

from .court_session import CourtSession


class CourtListener:
    """
    Main object for constructing the requests instance and session for creating
    the HTTP API call to the courtlistener endpoint
    """

    def __init__(self, court_session: CourtSession = None):
        self.__court_session = court_session

    def load_api_key(self, courtlistener_env: str = None) -> str:
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

    @property
    def court_session(self) -> CourtSession:
        """
        Court Session property instance for the CourtListener
        object. Essentially a container around the REST API
        request
        """
        if self.__court_session is None:
            default_api_key = self.load_api_key("COURTLISTENER")
            default_authorization = {"Authorization": f"Token {default_api_key}"}

            court_session_instance = CourtSession(
                endpoint_base="https://www.courtlistener.com/",
                api_key=default_api_key,
                headers=default_authorization,
                parameters={},
            )
            self.__court_session = court_session_instance
            logger.debug(f"Setting default court session {self.__court_session}")
        return self.__court_session

    def __enter__(self):
        """
        Entrypoint for starting courtlistener sessions
        """
        pass

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        Exitpoint for terminating courtlistener sessions
        """
        pass

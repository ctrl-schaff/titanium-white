"""
Collection of classes for implementating the wrapper around
the courtlistener API
"""
import os

from loguru import logger
import requests


class CourtSession:
    """
    Wrapper class around a request.Session instance
    Main object for constructing the requests instance and session for creating
    the HTTP API call to the courtlistener endpoint

    Constructor takes the courtlistener API key as a string argument. If no arguments
    are passed to the constructor, then the object will attempt to load the api key
    from the local environment via the COURTLISTENER environment variable
    """

    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = self.__load_api_key("COURTLISTENER")
        self.api_key = api_key
        self.http_session = requests.Session()

    @classmethod
    def __load_api_key(cls, courtlistener_env: str = None) -> str:
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

    def __enter__(self):
        """
        Context management entry point

        Returns the same CourtSession instance back to the caller
        Identical to the requests.Session __enter__ method:
        https://github.com/psf/requests/blob/v2.28.2/requests/sessions.py#L452
        """
        return self

    def __exit__(self, *args, **kwargs):
        """
        Context management exit point

        Cleans up the session instance
        Same logic used as the requests.Session __close__ method
        https://github.com/psf/requests/blob/v2.28.2/requests/sessions.py#L794
        """
        for adapter in self.http_session.adapters.values():
            logger.debug("Closing adapter {adapter}")
            adapter.close()

    def get_query(self, **kwargs):
        """
        Prepares the GET request and sends the query to the courtlistener API endpoint,
        and then processes the response

        Supports the same input arguments as the requests.Request method except the method
        parameter, as this one is hard-coded for HTTP "GET"
        |  :param url: URL to send.
        |  :param headers: dictionary of headers to send.
        |  :param files: dictionary of {filename: fileobject} files to multipart upload.
        |  :param data: the body to attach to the request. If a dictionary or
        |      list of tuples ``[(key, value)]`` is provided, form-encoding will
        |      take place.
        |  :param json: json for the body to attach to the request
        |               (if files or data is not specified).
        |  :param params: URL parameters to append to the URL. If a dictionary or
        |      list of tuples ``[(key, value)]`` is provided, form-encoding will
        |      take place.
        |  :param auth: Auth handler or (user, pass) tuple.
        |  :param cookies: dictionary or CookieJar of cookies to attach to this request.
        |  :param hooks: dictionary of callback hooks, for internal usage.
        """
        query_args = self.__inject_authorization(kwargs)
        query_args["method"] = "GET"

        request_instance = requests.Request(**query_args)

        prepared_request_instance = self.http_session.prepare_request(request_instance)

        # Merge environment settings into session
        settings = self.http_session.merge_environment_settings(
            prepared_request_instance.url, {}, None, None, None
        )
        response_instance = self.http_session.send(prepared_request_instance, **settings)
        return response_instance, prepared_request_instance

    def __inject_authorization(self, query_args: dict) -> dict:
        """
        Ensures that the api_key is properly inserted into the request if the user didn't
        specify the "Authorization" field in the headers section of the request

        The "headers" argument has to be a dictionary so we should always assume that the
        argument is either a dictionary we can update or None

        """
        authorization_field = {"Authorization": f"Token: {self.api_key}"}
        if query_args.get("headers", None):
            query_args["headers"].update(authorization_field)
        else:
            query_args["headers"] = authorization_field
        return query_args

"""
Wrapper class for handling the REST session construction for usage
within the CourtListener class
"""

from dataclasses import dataclass

import requests
from requests.adapters import HTTPAdapter


class CourtSessionTimeoutAdapter(HTTPAdapter):
    """
    Overloaded HTTPAdapter for requests.Session instances
    to ensure we always have a default timeout if not specified
    """

    DEFAULT_TIMEOUT_SEC = 5

    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop("timeout", self.DEFAULT_TIMEOUT_SEC)
        super().__init__(*args, **kwargs)

    def send(self, request: requests.Request, **kwargs):
        kwargs["timeout"] = kwargs.get("timeout", self.timeout)
        return super().send(request, **kwargs)


@dataclass(repr=True, eq=True, frozen=True, kw_only=True)
class CourtSession:
    """
    Basic data class for storing the API information
    required for accessing the CourtListener third party
    API
    """

    endpoint_base: str
    api_key: str
    headers: dict
    parameters: dict

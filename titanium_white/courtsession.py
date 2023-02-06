"""
Wrapper class for handling the REST session construction for usage
within the CourtListener class
"""

from dataclasses import dataclass


@dataclass(repr=True, eq=True, frozen=True, kw_only=True)
class CourtSession:
    """
    Basic data class for storing the API information
    required for accessing the CourtListener third party
    API
    """

    endpoint: str
    api_key: str
    headers: dict
    parameters: dict

"""
Asynchronous version of our CourtSession object

Leverages aiohttp and asyncio to perform concurrent requests
against the courtlistener API
"""
import asyncio
import json
import math

import aiohttp
from loguru import logger

from .authorization import load_api_key


class CourtPool:
    """
    Wrapper class around a request.Session instance
    Main object for constructing the requests instance and session for creating
    the HTTP API call to the courtlistener endpoint

    Constructor takes the courtlistener API key as a string argument. If no arguments
    are passed to the constructor, then the object will attempt to load the api key
    from the local environment via the COURTLISTENER environment variable

    Constructor Arguments:
    api_key = None
    --- (Overloaded Arguments) ---
    https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession
    base_url = None
    connector = None
    cookies = None
    headers = None
    skip_auto_headers=None
    auth=None
    json_serialize=json.dumps
    version=aiohttp.HttpVersion11
    cookie_jar=None
    read_timeout=None
    conn_timeout=None
    timeout=sentinel
    raise_for_status=False
    connector_owner=True
    auto_decompress=True
    read_bufsize=2**16
    requote_redirect_url=False
    trust_env=False
    trace_configs=None)
    """

    def __init__(self, api_key: str = None, **kwargs):
        if api_key is None:
            api_key = load_api_key("COURTLISTENER")
        self.api_key = api_key

        self.http_session = aiohttp.ClientSession(**kwargs)

    async def __aenter__(self):
        """
        Context management entry point

        Returns the same CourtSession instance back to the caller
        Identical to the requests.Session __enter__ method:
        https://github.com/psf/requests/blob/v2.28.2/requests/sessions.py#L452
        """
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Context management exit point

        Cleans up the session instance
        """
        await self.http_session.close()
        return None

    async def async_get_query(self, **kwargs):
        """
        Prepares the GET request and sends the query to the courtlistener API endpoint,
        and then processes the response

        Supports the same input arguments as the aiohttp.request method except the method
        parameter, as this one is hard-coded for HTTP "GET"

        page_depth = None
        --- (Overloaded Arguments) ---
        https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession
        method: str,
        str_or_url: StrOrURL,
        params: Optional[Mapping[str, str]] = None,
        data: Any = None,
        json: Any = None,
        cookies: Optional[LooseCookies] = None,
        headers: Optional[LooseHeaders] = None,
        skip_auto_headers: Optional[Iterable[str]] = None,
        auth: Optional[BasicAuth] = None,
        allow_redirects: bool = True,
        max_redirects: int = 10,
        compress: Optional[str] = None,
        chunked: Optional[bool] = None,
        expect100: bool = False,
        raise_for_status: Union[
            None, bool, Callable[[ClientResponse], Awaitable[None]]
        ] = None,
        read_until_eof: bool = True,
        proxy: Optional[StrOrURL] = None,
        proxy_auth: Optional[BasicAuth] = None,
        timeout: Union[ClientTimeout, _SENTINEL, None] = sentinel,
        ssl: Optional[Union[SSLContext, bool, Fingerprint]] = None,
        proxy_headers: Optional[LooseHeaders] = None,
        trace_request_ctx: Optional[SimpleNamespace] = None,
        read_bufsize: Optional[int] = None,
        auto_decompress: Optional[bool] = None,
        """
        query_args = self.__inject_authorization(kwargs)
        query_args["method"] = "GET"

        page_depth = kwargs.pop("page_depth", 10)
        query_results = {"count": 0}
        logger.debug(f"Querying CourtListener:\n{json.dumps(query_args, indent=4)}")
        initial_response = await self.http_session.request(**query_args)

        json_body = await initial_response.json()
        query_results["count"] = json_body.get("count", 0)
        num_query_pages = math.ceil(query_results["count"] / 20)
        page_depth = min(page_depth, num_query_pages)

        query_url = initial_response.url
        logger.info(f"GET {query_url}")
        query_results[query_url] = json_body.get("results", None)

        for page_index in range(2, page_depth + 1):
            query_args["params"].update({"page": page_index})
            logger.info(f"GET {query_args.get('url', None)}")
            query_response = await self.http_session.request(**query_args)

            query_results[query_response.url] = await query_response.json()
            query_url = initial_response.url
            logger.info(f"GET {query_url}")
            query_results[query_url] = json_body.get("results", None)

        return query_results

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

import abc
from json import JSONDecodeError
from typing import Any, Dict

import aiohttp

from pyjwt_key_fetcher.errors import JWTHTTPFetchError


class HTTPClient(abc.ABC):
    """
    Abstract base class for HTTP Clients used to fetch the configuration and JWKs in
    JSON format.
    """

    @abc.abstractmethod
    async def get_json(self, url: str) -> Dict[str, Any]:
        """
        Get and parse JSON data from a URL.

        :param url: The URL to fetch the data from.
        :return: The JSON data as a dictionary.
        :raise JWTHTTPFetchError: If there's a problem fetching the data.
        """
        raise NotImplementedError


class DefaultHTTPClient(HTTPClient):
    """
    A default client implemented using aiohttp.
    """

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get_json(self, url: str) -> Dict[str, Any]:
        """
        Get and parse JSON data from a URL.

        :param url: The URL to fetch the data from.
        :return: The JSON data as a dictionary.
        :raise JWTHTTPFetchError: If there's a problem fetching or decoding the data.
        """
        if not (url.startswith("https://") or url.startswith("http://")):
            raise JWTHTTPFetchError("Unsupported protocol in 'iss'")

        try:
            async with self.session.get(url) as resp:
                data = await resp.json()
                if resp.status != 200:
                    raise JWTHTTPFetchError(f"Failed to fetch or decode {url}")
        except (aiohttp.ClientError, JSONDecodeError) as e:
            raise JWTHTTPFetchError(f"Failed to fetch or decode {url}") from e

        return data

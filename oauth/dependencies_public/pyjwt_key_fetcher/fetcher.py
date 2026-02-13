from typing import Any, Dict, Iterable, MutableMapping, Optional

import jwt
from cachetools import TTLCache

from pyjwt_key_fetcher.errors import JWTFormatError, JWTInvalidIssuerError
from pyjwt_key_fetcher.http_client import DefaultHTTPClient, HTTPClient
from pyjwt_key_fetcher.key import Key
from pyjwt_key_fetcher.provider import Provider


class AsyncKeyFetcher:
    def __init__(
        self,
        valid_issuers: Optional[Iterable] = None,
        http_client: Optional[HTTPClient] = None,
        cache_ttl: int = 3600,
        cache_maxsize: int = 32,
        config_path: str = "/.well-known/openid-configuration",
    ) -> None:
        """
        Initialize a new AsyncKeyFetcher.

        :param valid_issuers: Valid issuers, use None to not enforce any restrictions.
        :param http_client: A HTTPClient used to fetch JSON data, such as the
        configuration and JWKs.
        :param cache_ttl: The time-to-live value in seconds for cached items.
        :param cache_maxsize: The maximum size of the cache.
        :param config_path: The path from which the configuration is fetched from the
        issuer.
        """
        self.config_path = config_path

        if not http_client:
            http_client = DefaultHTTPClient()

        if not valid_issuers:
            valid_issuers = set()

        self._http_client = http_client
        self._valid_issuers = set(valid_issuers)
        self._cache: MutableMapping[str, Provider] = TTLCache(
            maxsize=cache_maxsize,
            ttl=cache_ttl,
        )

    @staticmethod
    def get_kid(token: str) -> str:
        """
        Get the kid from the token.

        :param token: The JWT token.
        :return: The kid (key id) from the token.
        :raise JWTFormatException: If the token doesn't have a "kid".
        :raise PyJWTError: If the token can't be decoded.
        """
        jwt_headers = jwt.get_unverified_header(token)
        try:
            kid = jwt_headers["kid"]
        except KeyError:
            raise JWTFormatError("Missing 'kid' in header")
        return kid

    def _validate_issuer(self, issuer: str) -> None:
        """
        Ensure the issuer is amongst the valid ones or raise an exception.

        :param issuer: The iss from the token.
        :raise JWTInvalidIssuerError: If the issuer is not valid.
        """
        if self._valid_issuers and issuer not in self._valid_issuers:
            raise JWTInvalidIssuerError(f"Invalid 'iss': '{issuer}'")

    @staticmethod
    def get_issuer(token: str) -> str:
        """
        Get the issuer from the token (without verification).

        :param token: The JWT token (as a string).
        :return: The issuer.
        :raise JWTFormatException: If the token doesn't have a valid "iss".
        :raise PyJWTError: If the token can't be decoded.
        """
        payload = jwt.decode(token, options={"verify_signature": False})
        try:
            issuer = payload["iss"]
        except KeyError:
            raise JWTFormatError("Missing 'iss' in payload")

        return issuer

    def _get_provider(self, iss: str) -> Provider:
        """
        Get the provider from the cache, or create a new one if it's missing.

        :param iss: The issuer.
        :return: The Provider.
        """
        self._validate_issuer(iss)
        try:
            provider = self._cache[iss]
        except KeyError:
            provider = Provider(iss, self._http_client, self.config_path)
            self._cache[iss] = provider

        return provider

    async def get_configuration(self, iss: str) -> Dict[str, Any]:
        """
        Get the configuration from the issuer.

        :param iss: The issuer of the token.
        :return: The configuration as a dictionary.
        :raise JWTHTTPFetchError: If there's a problem fetching the data.
        :raise JWTInvalidIssuerError: If the issuer is not valid.
        """
        provider = self._get_provider(iss)
        return await provider.get_configuration()

    async def get_key_by_iss_and_kid(self, iss: str, kid: str) -> Key:
        """
        Get the key based on "iss" and "kid".

        :param iss: The "iss" (issuer) of the JWT.
        :param kid: The "kid" (key id) from the header of the JWT.
        :return: The key.
        :raise JWTHTTPFetchError: If there's a problem fetching the data.
        :raise JWTKeyNotFoundError: If the kid is not found in the "jwks_uri"
        :raise JWTProviderError: If the data doesn't contain "jwks_uri".
        """
        provider = self._get_provider(iss)
        return await provider.get_key(kid)

    async def get_key(self, token: str) -> Key:
        """
        Get the key based on given token.

        :param token: The JWT as a string.
        :return: The key.
        :raise JWTFormatException: If the token doesn't have a "kid".
        :raise JWTFormatException: If the token doesn't have a valid "iss".
        :raise JWTHTTPFetchError: If there's a problem fetching the data.
        :raise JWTInvalidIssuerError: If the issuer is not valid.
        :raise JWTProviderError: If the data doesn't contain "jwks_uri".
        :raise PyJWTError: If the token can't be decoded.
        """
        kid = self.get_kid(token)
        iss = self.get_issuer(token)
        key = await self.get_key_by_iss_and_kid(iss=iss, kid=kid)
        return key

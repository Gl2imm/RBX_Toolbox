from typing import Any, Dict, Optional

import aiocache  # type: ignore

from pyjwt_key_fetcher.errors import (
    JWTKeyNotFoundError,
    JWTProviderConfigError,
    JWTProviderJWKSError,
)
from pyjwt_key_fetcher.http_client import HTTPClient
from pyjwt_key_fetcher.key import Key


class Provider:
    def __init__(
        self,
        iss: str,
        http_client: HTTPClient,
        config_path: str = "/.well-known/openid-configuration",
    ) -> None:
        self.iss = iss
        self.http_client = http_client
        self._configuration: Optional[Dict[str, Any]] = None
        self._jwk_map: Dict[str, Dict[str, Any]] = {}
        self.keys: Dict[str, Key] = {}
        self.config_path = config_path

    async def _config_uri(self) -> str:
        """
        Get the URI at which the configuration is expected to be found.

        Can be for example https://example.com/.well-known/openid-configuration
        :return: The configuration URI.
        """
        return f"{self.iss.rstrip('/')}{self.config_path}"

    async def get_configuration(self) -> Dict[str, Any]:
        """
        Get the configuration as a dictionary.

        :return: The configuration as a dictionary.
        :raise JWTHTTPFetchError: If there's a problem fetching the data.
        """
        if self._configuration is None:
            url = await self._config_uri()
            self._configuration = await self.http_client.get_json(url)

        return self._configuration

    async def _get_jwks_uri(self) -> str:
        """
        Retrieve the uri to JWKs.

        :return: The uri to the JWKs.
        :raise JWTHTTPFetchError: If there's a problem fetching the data.
        :raise JWTProviderConfigError: If the config doesn't contain "jwks_uri".
        """
        conf = await self.get_configuration()
        try:
            jwks_uri = conf["jwks_uri"]
        except KeyError as e:
            raise JWTProviderConfigError("Missing 'jwks_uri' in configuration") from e
        return jwks_uri

    @aiocache.cached(ttl=300)
    async def _fetch_jwk_map(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all JWKs for an issuer as a dictionary with kid as key.

        Rate limited to once per 5 minutes (300 seconds).

        :return: A mapping of {kid: {<data_for_the_kid>}, ...}
        :raise JWTHTTPFetchError: If there's a problem fetching the data.
        :raise JWTProviderConfigError: If the config doesn't contain "jwks_uri".
        :raise JWTProviderJWKSError: If the jwks_uri is missing the "jwks".
        """
        jwks_uri = await self._get_jwks_uri()
        data = await self.http_client.get_json(jwks_uri)
        try:
            jwks_list = data["keys"]
        except KeyError as e:
            raise JWTProviderJWKSError(f"Missing 'jwks' in {jwks_uri}") from e

        jwk_map = {jwk["kid"]: jwk for jwk in jwks_list}

        return jwk_map

    async def get_jwk_data(self, kid: str) -> Dict[str, Any]:
        """
        Get the raw data for a jwk based on kid.

        :param kid: The key ID.
        :return: The raw JWK data as a dictionary.
        :raise JWTHTTPFetchError: If there's a problem fetching the data.
        :raise JWTProviderConfigError: If the config doesn't contain "jwks_uri".
        :raise JWTProviderJWKSError: If the jwks_uri is missing the "jwks".
        :raise JWTKeyNotFoundError: If no matching kid was found.
        """
        if kid not in self._jwk_map:
            self._jwk_map = await self._fetch_jwk_map()
        try:
            return self._jwk_map[kid]
        except KeyError:
            raise JWTKeyNotFoundError

    async def get_key(self, kid: str) -> Key:
        """
        Get the Key for a particular kid.

        :param kid: The key id.
        :return: The Key.
        :raise JWTHTTPFetchError: If there's a problem fetching the data.
        :raise JWTProviderConfigError: If the config doesn't contain "jwks_uri".
        :raise JWTProviderJWKSError: If the jwks_uri is missing the "jwks".
        :raise JWTKeyNotFoundError: If no matching kid was found.
        """
        if kid not in self.keys:
            key = Key(await self.get_jwk_data(kid))
            self.keys[kid] = key

        return self.keys[kid]

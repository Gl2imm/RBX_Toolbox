class JWTKeyFetcherError(Exception):
    """Base class for JWTKeyFetcher errors"""


class JWTInvalidIssuerError(JWTKeyFetcherError):
    """Raised if the issuer is not valid"""


class JWTKeyNotFoundError(JWTKeyFetcherError):
    """Raised if no key could be found"""


class JWTFormatError(JWTKeyFetcherError):
    """Raised for keys that do not contain all kind of expected values"""


class JWTHTTPFetchError(JWTKeyFetcherError):
    """Raised if there's a problem doing http(s) requests"""


class JWTProviderConfigError(JWTKeyFetcherError):
    """Raised if expectations for configuration fields fail"""


class JWTProviderJWKSError(JWTKeyFetcherError):
    """Raised if expectations for JWKS fields fail"""

import jwt
import pytest

import pyjwt_key_fetcher
import pyjwt_key_fetcher.provider
from pyjwt_key_fetcher.errors import JWTInvalidIssuerError, JWTKeyNotFoundError


@pytest.mark.asyncio
async def test_fetching_key(create_provider_fetcher_and_client):
    provider, fetcher, client = await create_provider_fetcher_and_client()

    token = provider.create_token()
    key_entry = await fetcher.get_key(token)
    jwt.decode(token, audience=provider.aud, **key_entry)

    client.get_configuration.assert_called_once()
    client.get_jwks.assert_called_once()


@pytest.mark.asyncio
async def test_fetching_same_kid_only_once(create_provider_fetcher_and_client):
    provider, fetcher, client = await create_provider_fetcher_and_client()

    tokens = {provider.create_token() for _ in range(3)}
    for _ in range(2):
        for token in tokens:
            key_entry = await fetcher.get_key(token)
            jwt.decode(token, audience=provider.aud, **key_entry)

            client.get_configuration.assert_called_once()
            client.get_jwks.assert_called_once()


@pytest.mark.asyncio
async def test_fetching_after_issuing_new_key(create_provider_fetcher_and_client):
    provider, fetcher, client = await create_provider_fetcher_and_client()

    # Create first token and validate it
    token = provider.create_token()
    key_entry = await fetcher.get_key(token)
    jwt.decode(token, audience=provider.aud, **key_entry)

    client.get_configuration.assert_called_once()
    client.get_jwks.assert_called_once()

    # Make the provider roll out a new key
    provider.generate_new_key()

    # Get a new token, signed with the new key
    token_2 = provider.create_token()
    assert fetcher.get_kid(token) != fetcher.get_kid(token_2)

    # There's a ttl cache on the function to fetch JWKs, so validating the new
    # key should fail until that has expired
    with pytest.raises(JWTKeyNotFoundError):
        await fetcher.get_key(token_2)

    # Let's simulate the cache expired
    await pyjwt_key_fetcher.provider.Provider._fetch_jwk_map.cache.clear()

    # Now the the new token can be verified
    key_entry_2 = await fetcher.get_key(token_2)
    jwt.decode(token_2, audience=provider.aud, **key_entry_2)

    # Check the old token can be verified as well
    key_entry = await fetcher.get_key(token)
    jwt.decode(token, audience=provider.aud, **key_entry)

    # Verify we've fetched config only once and JWKs twice (once per "kid")
    assert client.get_configuration.call_count == 1
    assert client.get_jwks.call_count == 2


@pytest.mark.asyncio
async def test_fetching_from_multiple_issuers(
    create_provider_fetcher_and_client, create_provider
):
    provider, fetcher, client = await create_provider_fetcher_and_client()

    provider_2 = create_provider(client)

    token = provider.create_token()
    token_2 = provider_2.create_token()

    key_entry = await fetcher.get_key(token)
    key_entry_2 = await fetcher.get_key(token_2)
    jwt.decode(token, audience=provider.aud, **key_entry)
    jwt.decode(token_2, audience=provider_2.aud, **key_entry_2)

    # Verify we've fetched config and JWKs twice (once per issuer)
    assert client.get_configuration.call_count == 2
    assert client.get_jwks.call_count == 2


@pytest.mark.asyncio
async def test_issuer_validation(create_provider_fetcher_and_client, create_provider):
    valid_issuers = ["https://valid.example.com"]

    invalid_provider, fetcher, client = await create_provider_fetcher_and_client(
        valid_issuers=valid_issuers, iss="https://invalid.example.com"
    )
    valid_provider = create_provider(client, iss=valid_issuers[0])

    invalid_token = invalid_provider.create_token()
    valid_token = valid_provider.create_token()

    with pytest.raises(JWTInvalidIssuerError):
        await fetcher.get_key(invalid_token)
    assert client.get_configuration.call_count == 0
    assert client.get_jwks.call_count == 0

    key_entry = await fetcher.get_key(valid_token)
    jwt.decode(valid_token, audience=valid_provider.aud, **key_entry)

    assert client.get_configuration.call_count == 1
    assert client.get_jwks.call_count == 1

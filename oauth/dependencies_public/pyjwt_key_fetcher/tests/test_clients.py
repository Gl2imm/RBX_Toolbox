import json
from contextlib import asynccontextmanager
from typing import Optional
from unittest.mock import AsyncMock

import aiohttp
import pytest

from pyjwt_key_fetcher import DefaultHTTPClient
from pyjwt_key_fetcher.errors import JWTHTTPFetchError


@pytest.mark.asyncio
async def test_get_json_wrong_protocol():
    client = DefaultHTTPClient()
    with pytest.raises(JWTHTTPFetchError):
        await client.get_json("ftp://example.com")


def create_fake_session(
    payload: Optional[dict] = None,
    status_code: int = 200,
    exception: Optional[Exception] = None,
):
    if not payload:
        payload = {}

    @asynccontextmanager
    async def fake_get(url: str):
        if exception:
            raise exception

        fake_resp = AsyncMock()

        async def json_payload():
            return payload

        fake_resp.json = json_payload
        fake_resp.status = status_code

        yield fake_resp

    session_mock = AsyncMock(
        autospec=aiohttp.ClientSession(), wraps=aiohttp.ClientSession
    )
    session_mock.get = fake_get
    return session_mock


@pytest.mark.asyncio
async def test_get_valid_json():
    payload = {"hi": "there"}

    client = DefaultHTTPClient()
    client.session = create_fake_session(payload)
    assert payload == await client.get_json("https://example.com")


@pytest.mark.asyncio
async def test_get_not_200():
    payload = {"OH NO!": "NOT 200 OK"}

    client = DefaultHTTPClient()
    client.session = create_fake_session(payload, status_code=404)
    with pytest.raises(JWTHTTPFetchError):
        await client.get_json("https://example.com")


@pytest.mark.parametrize(
    "exception",
    [
        aiohttp.ClientError(),
        json.JSONDecodeError(
            "Expecting property name enclosed in double quotes", "{", 1
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_aio_error(exception):
    client = DefaultHTTPClient()
    client.session = create_fake_session(exception=exception)
    with pytest.raises(JWTHTTPFetchError):
        await client.get_json("https://example.com")

# Copyright © 2023 Roblox Corporation

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the “Software”), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# SPDX-License-Identifier: MIT

if "bpy" in locals():
    # Imports have run before. Need to reload the imported modules
    import importlib

    if "certifi" in locals():
        importlib.reload(certifi)
    if "aiohttp" in locals():
        importlib.reload(aiohttp)

import bpy
import ssl
import socket


def _make_fallback_resolver():
    """
    Returns a custom resolver for aiohttp 3.10+ that retries with IPv4-only on DNS failure.

    aiohttp 3.10+ changed the default resolver to use socket.getaddrinfo() inside a
    thread pool. On some Windows machines this thread-pool DNS call fails even though
    the system DNS works fine. Retrying with AF_INET (IPv4 only) works around the issue.
    Returns None on older aiohttp so the default connector behaviour is unchanged.
    """
    try:
        import aiohttp.abc
        from aiohttp.resolver import ThreadedResolver

        class _FallbackResolver(aiohttp.abc.AbstractResolver):
            def __init__(self):
                self._inner = ThreadedResolver()

            async def resolve(self, host, port=0, family=socket.AF_UNSPEC):
                try:
                    return await self._inner.resolve(host, port, family)
                except OSError:
                    # Retry IPv4-only — fixes thread-pool DNS failure on some Windows machines
                    return await self._inner.resolve(host, port, socket.AF_INET)

            async def close(self):
                await self._inner.close()

        return _FallbackResolver()
    except (ImportError, AttributeError):
        # aiohttp < 3.10 — ThreadedResolver doesn't exist, default behaviour is fine
        return None


def create_http_client():
    """Returns a new aiohttp ClientSession that uses certifi SSL context"""
    import certifi
    import aiohttp

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    resolver = _make_fallback_resolver()
    connector = aiohttp.TCPConnector(ssl=ssl_context, **({'resolver': resolver} if resolver else {}))

    return aiohttp.ClientSession(connector=connector)

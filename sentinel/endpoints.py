"""A provider endpoint must be an http:// or https:// address (ESR-0062 WP2,
EIP-ESR0062-002 F3; WR-ESR0061-002 F3).

`urllib` would otherwise open `file://` or `ftp://`. Kept inside `sentinel`,
which does not depend on `jarvis`, so it stays extractable.
"""

from __future__ import annotations

import urllib.parse

from sentinel.providers import ProviderError


def require_http_endpoint(endpoint: str, provider: str) -> str:
    """Return `endpoint`, or raise a non-retryable ProviderError that never
    repeats the address (it may hold a user name or password)."""

    try:
        parsed = urllib.parse.urlparse(endpoint)
        hostname = parsed.hostname
    except ValueError:
        parsed, hostname = None, None
    if parsed is None or parsed.scheme.lower() not in {"http", "https"} or not hostname:
        msg = f"{provider} endpoint must start with http:// or https:// and name a host."
        raise ProviderError(msg, transient=False)
    return endpoint

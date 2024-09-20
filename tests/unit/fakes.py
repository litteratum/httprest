"""Fakes for tests."""

from dataclasses import dataclass
from typing import Optional

from httprest import API
from httprest.http.fake_client import FakeHTTPClient


class _TestAPI(API):
    """API client for tests."""

    def make_call(self):
        """Make API call."""
        return self._request(
            "POST", "/example/endpoint/", json={"k": "v"}, headers={"h": "v"}
        )


@dataclass
class _APIComponents:
    """API components."""

    api: _TestAPI
    base_url: str
    http_client: FakeHTTPClient


def build_api(
    base_url: str = "http://base.com",
    http_client: Optional[FakeHTTPClient] = None,
) -> _APIComponents:
    """Build API client."""
    http_client = http_client or FakeHTTPClient()
    return _APIComponents(
        _TestAPI(base_url, http_client),
        base_url,
        http_client,
    )

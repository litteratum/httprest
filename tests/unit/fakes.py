"""Fakes for tests."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from httprest import API
from httprest.http import HTTPClient
from httprest.http.base import HTTPResponse


class _TestAPI(API):
    """API client for tests."""

    def make_call(self):
        """Make API call."""
        return self._request(
            "POST", "/example/endpoint/", json={"k": "v"}, headers={"h": "v"}
        )


class FakeHTTPClient(HTTPClient):
    """Fake HTTP client."""

    def __init__(self, responses: Optional[List[HTTPResponse]] = None) -> None:
        super().__init__()
        self.history: List[Dict[str, Optional[Any]]] = []
        self._responses = responses or [HTTPResponse(200, b"", {})]

    def _request(
        self,
        method: str,
        url: str,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> HTTPResponse:
        self.history.append(
            {
                "_method": "_request",
                "method": method,
                "url": url,
                "json": json,
                "headers": headers,
            }
        )

        return self._responses.pop(0)


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

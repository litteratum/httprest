"""Tests for the `urllib` HTTP client."""

import json as jsonlib
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator, Optional
from unittest.mock import MagicMock, patch

from httprest.http.auth import BasicAuth
from httprest.http.urllib_client import UrllibHTTPClient


@dataclass
class ClientComponents:
    """Client components.

    Consists of the client itself + patched `urllib.request`.
    """

    client: UrllibHTTPClient
    urllib_request: MagicMock


class UrllibResponse:
    """`urllib.request` response."""

    def __init__(
        self,
        status: int = 200,
        data: bytes = b"",
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> None:
        self.status = status
        self.data = data
        self.headers = headers or {}

        if json:
            self.headers["Content-Type"] = "application/json"
            self.data = jsonlib.dumps(json).encode()

    def read(self) -> bytes:
        """Read the response body."""
        return self.data


@contextmanager
def patched_client(
    request_timeout: float = 5, response: Optional[UrllibResponse] = None
) -> Iterator[ClientComponents]:
    """Return patched client."""
    with patch(
        "httprest.http.urllib_client.urllib.request", new=MagicMock()
    ) as mock:
        mock.urlopen.return_value.__enter__.return_value = (
            response or UrllibResponse()
        )
        yield ClientComponents(
            client=UrllibHTTPClient(request_timeout), urllib_request=mock
        )


def test_json_request():
    """Test for the JSON request."""
    with patched_client(
        request_timeout=2, response=UrllibResponse(json={"k": "v"})
    ) as comps:
        comps.urllib_request.Request.return_value = "mocked"

        resp = comps.client.request(
            "get",
            "http://example.com",
            json={"k": "v"},
            headers={"X-Test": "test"},
            params={"p": "example value"},
            auth=BasicAuth("user", "__secret__"),
        )
        assert resp.status_code == 200
        assert resp.json == {"k": "v"}

    comps.urllib_request.Request.assert_called_once_with(
        "http://example.com?p=example+value",
        data=b'{"k": "v"}',
        headers={
            "X-Test": "test",
            "Content-Type": "application/json",
            "Authorization": "Basic dXNlcjpfX3NlY3JldF9f",
        },
        method="GET",
    )
    comps.urllib_request.urlopen.assert_called_once_with("mocked", timeout=2)

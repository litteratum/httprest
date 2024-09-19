"""Fake client."""

from typing import Any, Dict, List, Optional, Union

from httprest.http.base import HTTPResponse

from .base import HTTPClient, HTTPTimeoutError


class FakeHTTPClient(HTTPClient):
    """Fake HTTP client."""

    def __init__(
        self, responses: Optional[List[Union[Exception, HTTPResponse]]] = None
    ) -> None:
        # pylint:disable=super-init-not-called
        self.history: List[Dict[str, Optional[Any]]] = []
        self._responses = responses

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
        if not self._responses:
            raise HTTPTimeoutError("No response provided")

        response = self._responses.pop(0)
        if isinstance(response, Exception):
            raise response

        return response

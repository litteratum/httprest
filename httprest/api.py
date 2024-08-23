"""API."""

from typing import Optional as _Optional

from httprest.http import HTTPClient as _HTTPClient
from httprest.http import HTTPResponse as _HTTPResponse
from httprest.http.urllib_client import UrllibHTTPClient as _UrllibHTTPClient


class API:
    """API.

    This class is used to communicated with the API.
    """

    def __init__(
        self, base_url: str, http_client: _Optional[_HTTPClient] = None
    ) -> None:
        """Init API.

        :param base_url: API base URL
        :param http_client: HTTP client to use for making HTTP requests.
          If not provided, the default one will be used
        """
        self._base_url = base_url.rstrip("/")
        self._http_client = http_client or _UrllibHTTPClient()

    def _request(
        self,
        method: str,
        endpoint: str,
        json: _Optional[dict] = None,
        headers: _Optional[dict] = None,
    ) -> _HTTPResponse:
        """Make API request.

        :param method: request HTTP method (case-insensitive)
        :param endpoint: API endpoint. Will be appended to the base URL
        :param json: JSON data to send in the request body
        """
        return self._http_client.request(
            method, self._build_url(endpoint), json, headers
        )

    def _build_url(self, endpoint: str) -> str:
        return f"{self._base_url}/{endpoint.strip('/')}"

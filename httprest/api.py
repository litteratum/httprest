"""API."""

from typing import Optional as _Optional

from httprest.http import HTTPClient as _HTTPClient
from httprest.http import HTTPResponse as _HTTPResponse
from httprest.http.auth import BaseAuth as _BaseAuth
from httprest.http.cert import ClientCertificate as _ClientCertificate
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
        params: _Optional[dict] = None,
        auth: _Optional[_BaseAuth] = None,
        cert: _Optional[_ClientCertificate] = None,
    ) -> _HTTPResponse:
        # pylint: disable=too-many-arguments
        """Make API request.

        :param endpoint: API endpoint. Will be appended to the base URL

        Other parameters are the same as for the `HTTPClient.request` method
        """
        return self._http_client.request(
            method=method,
            url=self._build_url(endpoint),
            json=json,
            headers=headers,
            params=params,
            auth=auth,
            cert=cert,
        )

    def _build_url(self, endpoint: str) -> str:
        return f"{self._base_url}/{endpoint.strip('/')}"

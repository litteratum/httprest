"""HTTP client which uses `requests` under the hood."""

from types import ModuleType
from typing import Optional, Union

import requests

from httprest.http import errors as _errors

from .base import HTTPClient, HTTPResponse
from .cert import ClientCertificate
from .timeout import Timeout


class RequestsHTTPClient(HTTPClient):
    """`requests` HTTP client.

    By default a reusable ``requests.Session`` is used (connection reuse).
    Pass ``requester`` to override this:

    * a custom ``requests.Session`` (e.g. with retries/adapters configured), or
    * the ``requests`` module itself, to make independent module-level calls
      with no connection reuse.
    """

    def __init__(
        self,
        timeout: Optional[Timeout] = None,
        requester: Optional[Union[requests.Session, ModuleType]] = None,
    ) -> None:
        super().__init__(timeout)
        self._requester = (
            requester if requester is not None else requests.Session()
        )

    def _request(
        self,
        method: str,
        url: str,
        data: Optional[Union[dict, bytes]] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        cert: Optional[ClientCertificate] = None,
    ) -> HTTPResponse:
        # pylint: disable=too-many-arguments
        client_cert = None
        if cert:
            client_cert = (
                cert.cert_path
                if cert.key_path is None
                else (cert.cert_path, cert.key_path)
            )
        try:
            response: requests.Response = getattr(
                self._requester, method.lower()
            )(
                url,
                data=data,
                json=json,
                timeout=(
                    (self._timeout.connect, self._timeout.read)
                    if self._timeout
                    else None
                ),
                headers=headers,
                cert=client_cert,
            )
        except ConnectionError as exc:
            raise _errors.HTTPConnectionError(exc) from exc
        except requests.Timeout as exc:
            raise _errors.HTTPTimeoutError(exc) from exc
        except requests.RequestException as exc:
            raise _errors.HTTPRequestError(exc) from exc

        return HTTPResponse(
            response.status_code, response.content, dict(response.headers)
        )

    def __str__(self) -> str:
        return self.__class__.__name__

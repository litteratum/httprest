"""HTTP errors."""


class HTTPRequestError(Exception):
    """Base HTTP request error."""


class HTTPConnectionError(HTTPRequestError):
    """Any error related to connection."""


class HTTPTimeoutError(HTTPRequestError):
    """HTTP request timed out."""


class HTTPInvalidResponseError(HTTPRequestError):
    """HTTP response is invalid."""


class HTTPError(HTTPRequestError):
    """HTTP error based on the status code."""

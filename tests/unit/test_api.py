"""Tests for the API client."""

import typing

import pytest

from httprest.http import HTTPResponse

from .fakes import FakeHTTPClient, build_api


def test_api_call():
    """Test API call."""
    comps = build_api(
        base_url="http://fake.com/",
        http_client=FakeHTTPClient(responses=[HTTPResponse(200, b"", {})]),
    )
    comps.api.make_call()

    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": {"h": "v"},
            "json": {"k": "v"},
            "method": "POST",
            "url": "http://fake.com/example/endpoint/",
        },
    ]


@pytest.mark.parametrize("endpoint", ["", None])
def test_url_without_endpoint(endpoint: typing.Optional[str]):
    """Test for request URL when endpoint is not specified.

    The base URL must be used.
    """
    base = "http://fake.com"
    comps = build_api(
        base_url=base,
        http_client=FakeHTTPClient(responses=[HTTPResponse(200, b"", {})]),
    )
    comps.api.make_call(endpoint=endpoint)
    assert comps.http_client.history[0]["url"] == base

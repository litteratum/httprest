"""Tests for the API client."""

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
            "cert": None,
            "url": "http://fake.com/example/endpoint",
        },
    ]

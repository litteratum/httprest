"""Tests for the API client."""

from .fakes import build_api


def test_api_call():
    """Test API call."""
    comps = build_api(base_url="http://fake.com/")
    comps.api.make_call()

    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": {"h": "v"},
            "json": {"k": "v"},
            "method": "POST",
            "url": "http://fake.com/example/endpoint",
        },
    ]

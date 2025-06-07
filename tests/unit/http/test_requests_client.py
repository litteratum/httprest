"""Tests for the `requests` HTTP client."""

import pytest
import requests
import responses
from responses import matchers

from httprest.http.errors import HTTPTimeoutError
from httprest.http.requests_client import RequestsHTTPClient


@responses.activate
def test_success_post_json():
    """Test successful post_json."""
    responses.post(
        "https://example.com",
        json={"k": "v"},
        match=[
            matchers.json_params_matcher({}),
            matchers.header_matcher({"Content-Type": "application/json"}),
        ],
    )
    response = RequestsHTTPClient().request(
        "post", "https://example.com", json={}
    )
    assert response.status_code == 200
    assert response.json == {"k": "v"}


@responses.activate
def test_unsuccessful_post_json():
    """Test unsuccessful post_json."""
    responses.post("https://example.com", json={"k": "v"}, status=400)
    response = RequestsHTTPClient().request(
        "post", "https://example.com", json={}
    )
    assert response.status_code == 400
    assert response.json == {"k": "v"}


@responses.activate
def test_post_json_timeout():
    """Test post_json timeout."""
    responses.post("https://example.com", body=requests.Timeout(), status=400)

    with pytest.raises(HTTPTimeoutError):
        RequestsHTTPClient().request("post", "https://example.com", json={})


@responses.activate
def test_get_ok():
    """Test successful get."""
    responses.add(responses.GET, "https://example.com", json={"k": "v"})
    response = RequestsHTTPClient().request("get", "https://example.com")
    assert response.status_code == 200
    assert response.json == {"k": "v"}


@responses.activate
def test_form_data():
    """Test successful get."""
    responses.post(
        "https://example.com",
        json={"k": "v"},
        match=[matchers.urlencoded_params_matcher({"k": "v"})],
    )
    response = RequestsHTTPClient().request(
        "post", "https://example.com", data={"k": "v"}
    )
    assert response.status_code == 200

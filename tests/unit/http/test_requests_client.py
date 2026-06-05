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


@responses.activate
def test_query_params():
    """Test query params."""
    responses.get(
        "https://example.com",
        match=[matchers.query_param_matcher({"p": "hello/world"})],
    )
    response = RequestsHTTPClient().request(
        "get", "https://example.com", params={"p": "hello/world"}
    )
    assert response.status_code == 200


@responses.activate
def test_requester_module():
    """Test using the `requests` module directly (no session)."""
    responses.add(responses.GET, "https://example.com", json={"k": "v"})
    client = RequestsHTTPClient(requester=requests)
    response = client.request("get", "https://example.com")
    assert response.status_code == 200
    assert response.json == {"k": "v"}


@responses.activate
def test_injected_session_is_used():
    """An injected session must be the one actually performing the request.

    The session carries a custom header that a default, internally-created
    session would not have. The request is only matched (and succeeds) if it
    goes through this exact session, so matching proves it is used -- no need
    to inspect the client's internals.
    """
    responses.get(
        "https://example.com",
        json={"k": "v"},
        match=[matchers.header_matcher({"X-Custom": "v"})],
    )
    session = requests.Session()
    session.headers["X-Custom"] = "v"
    client = RequestsHTTPClient(requester=session)
    response = client.request("get", "https://example.com")
    assert response.status_code == 200

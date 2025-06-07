"""Tests for the response module."""

import json as jsonlib

import pytest

from httprest.http import HTTPResponse
from httprest.http.errors import HTTPClientError, HTTPInvalidResponseError


def test_ok():
    """Test for the ok property."""
    assert HTTPResponse(200, b"", {}).ok
    assert not HTTPResponse(400, b"", {}).ok


def test_raise_for_status():
    """Test for the raise_for_status method."""
    resp = HTTPResponse(400, b"", {})
    with pytest.raises(HTTPClientError) as exc:
        resp.raise_for_status()

    assert exc.value.status_code == 400


class TestJSON:
    """Tests for the `json` property."""

    def test_no_content_type_json_is_none(self):
        """Test for the content type.

        If it is not application/json, the json will be None.
        """
        assert (
            HTTPResponse(200, jsonlib.dumps({"k": "v"}).encode(), {}).json
            is None
        )

    def test_content_type_is_json_but_body_is_not_json(self):
        """Test for the non-json body.

        If the content type is application/json, but body does not contain
        JSON, an exception is expected.
        """
        with pytest.raises(HTTPInvalidResponseError, match="Invalid JSON"):
            _ = HTTPResponse(
                200, b"", {"Content-Type": "application/json;utf8"}
            ).json

    def test_ok(self):
        """Test the OK JSON load case."""
        assert HTTPResponse(
            200,
            jsonlib.dumps({"k": "v"}).encode(),
            {"Content-Type": "application/json;utf8"},
        ).json == {"k": "v"}

    def test_json_is_lazy(self):
        """Test that `json` is lazily evaluated."""
        response = HTTPResponse(
            200,
            jsonlib.dumps({"k": "v"}).encode(),
            {"Content-Type": "application/json;utf8"},
        )
        # request json
        first_json = response.json
        # change the body
        response.body = jsonlib.dumps({"changed": "body"}).encode()
        # request json again. It must not change
        assert first_json == response.json

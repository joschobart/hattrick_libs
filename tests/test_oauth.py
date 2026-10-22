"""Contract tests for ht_libs.do_hattrick_request (no network).

requests.Session.send is replaced by a fake transport: the real
requests-oauthlib signing runs, but nothing ever leaves the machine.
"""

from urllib.parse import parse_qs, unquote

import pytest
import requests

from ht_libs import config, do_hattrick_request


class FakeTransport:
    """Records every prepared request and answers with a canned body."""

    def __init__(self):
        self.body = ""
        self.requests = []

    def respond(self, request):
        self.requests.append(request)
        response = requests.Response()
        response.status_code = 200
        response._content = self.body.encode()
        response.encoding = "utf-8"
        response.url = request.url
        response.request = request
        return response


@pytest.fixture
def transport(monkeypatch):
    fake = FakeTransport()

    def send(session, request, **kwargs):
        return fake.respond(request)

    monkeypatch.setattr(requests.Session, "send", send)
    return fake


def oauth_params(request):
    """Parse the `Authorization: OAuth k="v", ...` header into a dict."""
    header = request.headers["Authorization"]
    if isinstance(header, bytes):
        header = header.decode()
    assert header.startswith("OAuth ")
    pairs = (item.strip().split("=", 1) for item in header[len("OAuth ") :].split(","))
    return {key: unquote(value.strip('"')) for key, value in pairs}


def test_fetch_authorize_url(transport):
    transport.body = "oauth_token=req-token&oauth_token_secret=req-secret"

    token, secret, url = do_hattrick_request.fetch_authorize_url(
        scope="manage_challenges"
    )

    assert (token, secret) == ("req-token", "req-secret")
    base, _, query = url.partition("?")
    assert base == config.AUTHORIZE_URL
    assert parse_qs(query) == {
        "scope": ["manage_challenges"],
        "oauth_token": ["req-token"],
    }

    (request,) = transport.requests
    assert request.url == config.REQUEST_TOKEN_URL
    params = oauth_params(request)
    assert params["oauth_consumer_key"] == config.OAUTH_KEY
    assert params["oauth_callback"] == "oob"
    assert params["oauth_signature_method"] == "HMAC-SHA1"
    assert params["oauth_signature"]


def test_get_access_token(transport):
    transport.body = "oauth_token=acc-key&oauth_token_secret=acc-secret"

    result = do_hattrick_request.get_access_token("req-token", "req-secret", "1234")

    assert result == ("acc-key", "acc-secret")
    (request,) = transport.requests
    assert request.url == config.ACCESS_TOKEN_URL
    params = oauth_params(request)
    assert params["oauth_token"] == "req-token"
    assert params["oauth_verifier"] == "1234"


def test_open_auth_session_signs_chpp_requests(transport):
    transport.body = "<HattrickData/>"
    session = do_hattrick_request.open_auth_session("acc-key", "acc-secret")

    response = session.get(
        config.BASE_URL, params={"file": "matchdetails", "version": "3.1"}
    )

    assert response.text == "<HattrickData/>"
    (request,) = transport.requests
    assert request.method == "GET"
    base, _, query = request.url.partition("?")
    assert base == config.BASE_URL
    assert parse_qs(query) == {"file": ["matchdetails"], "version": ["3.1"]}
    params = oauth_params(request)
    assert params["oauth_token"] == "acc-key"
    assert "oauth_verifier" not in params

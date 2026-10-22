"""Contract tests for ht_libs.do_hattrick_request.

The OAuth client is replaced by a fake, so no network is needed. These tests
pin the public function signatures and return values.
"""

from ht_libs import do_hattrick_request


class FakeOAuthService:
    """Records calls and returns canned tokens instead of talking to CHPP."""

    def __init__(self):
        self.calls = []

    def get_request_token(self, params):
        self.calls.append(("get_request_token", params))
        return "req-token", "req-secret"

    def get_authorize_url(self, request_token, scope):
        self.calls.append(("get_authorize_url", request_token, scope))
        return f"https://example.invalid/authorize?oauth_token={request_token}"

    def get_access_token(self, request_token, request_token_secret, params):
        self.calls.append(
            ("get_access_token", request_token, request_token_secret, params)
        )
        return "acc-key", "acc-secret"


def test_fetch_authorize_url(monkeypatch):
    fake = FakeOAuthService()
    monkeypatch.setattr(do_hattrick_request, "request_client", fake)

    result = do_hattrick_request.fetch_authorize_url(scope="manage_challenges")

    assert result == (
        "req-token",
        "req-secret",
        "https://example.invalid/authorize?oauth_token=req-token",
    )
    assert fake.calls == [
        ("get_request_token", {"oauth_callback": "oob"}),
        ("get_authorize_url", "req-token", "manage_challenges"),
    ]


def test_get_access_token(monkeypatch):
    fake = FakeOAuthService()
    monkeypatch.setattr(do_hattrick_request, "request_client", fake)

    result = do_hattrick_request.get_access_token("req-token", "req-secret", "1234")

    assert result == ("acc-key", "acc-secret")
    assert fake.calls == [
        ("get_access_token", "req-token", "req-secret", {"oauth_verifier": "1234"}),
    ]


def test_open_auth_session_returns_session_with_get():
    session = do_hattrick_request.open_auth_session("acc-key", "acc-secret")
    assert callable(session.get)

"""Functions for OAUTH-authentication on hattrick.org (CHPP, OAuth 1.0a)."""

from requests_oauthlib import OAuth1Session

from . import config


def _client(**kwargs):
    """Create an OAuth1Session signed with this app's consumer credentials."""
    return OAuth1Session(
        config.OAUTH_KEY,
        client_secret=config.OAUTH_SECRET,
        **kwargs,
    )


def fetch_authorize_url(oauth_url="oob", scope=""):
    """Function for OAUTH Step 1 and 2.

    Step 1: Fetch Temporary Credential.
    Step 2: Get the auth URL.

    :param oauth_url: Default value = "oob")
    :param scope: Default value = "")
    :returns: request_token, request_token_secret, authorize_url
    :raises:
    """
    oauth = _client(callback_uri=oauth_url)
    tokens = oauth.fetch_request_token(config.REQUEST_TOKEN_URL)

    request_token = tokens["oauth_token"]
    request_token_secret = tokens["oauth_token_secret"]
    authorize_url = oauth.authorization_url(config.AUTHORIZE_URL, scope=scope)

    return request_token, request_token_secret, authorize_url


def get_access_token(request_token, request_token_secret, auth_pin):
    """Function for OAUTH Step 3 and 4.

    Step 3 : Save auth_pin in var after the client was authorized.
    Step 4 : Exchange the request token for an access token.

    :param request_token:
    :param request_token_secret:
    :param auth_pin:
    :returns: access_token_key, access_token_secret
    :raises:
    """
    oauth = _client(
        resource_owner_key=request_token,
        resource_owner_secret=request_token_secret,
    )
    tokens = oauth.fetch_access_token(config.ACCESS_TOKEN_URL, verifier=auth_pin)

    return tokens["oauth_token"], tokens["oauth_token_secret"]


def open_auth_session(access_token_key, access_token_secret):
    """Function for OAUTH Step 5.

    Finally open OAUTH-session.

    :param access_token_key:
    :param access_token_secret:
    :returns: auth_session (a requests.Session, so .get(url, params=...) works as before)
    :raises:
    """
    return _client(
        resource_owner_key=access_token_key,
        resource_owner_secret=access_token_secret,
    )

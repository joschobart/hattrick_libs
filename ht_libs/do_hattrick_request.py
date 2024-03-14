""" Functions for OAUTH-authentication on hattrick.org. """


from rauth import OAuth1Service  # type: ignore
from rauth import OAuth1Session

from . import config

request_client = OAuth1Service(
    consumer_key=config.OAUTH_KEY,
    consumer_secret=config.OAUTH_SECRET,
    request_token_url=config.REQUEST_TOKEN_URL,
    access_token_url=config.ACCESS_TOKEN_URL,
    authorize_url=config.AUTHORIZE_URL,
    base_url=config.BASE_URL,
)


def fetch_authorize_url(oauth_url="oob", scope=""):
    """Function for OAUTH Step 1 and 2.

    Step 1: Fetch Temporary Credential.
    Step 2: Get the auth URL.

    :param oauth_url: Default value = "oob")
    :param scope: Default value = "")
    :returns: request_token, request_token_secret
    :raises:
    """
    request_token, request_token_secret = request_client.get_request_token(
        params={
            "oauth_callback": oauth_url,
        }
    )

    authorize_url = request_client.get_authorize_url(request_token, scope=scope)

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
    access_token_key, access_token_secret = request_client.get_access_token(
        request_token, request_token_secret, params={"oauth_verifier": auth_pin}
    )

    return access_token_key, access_token_secret


def open_auth_session(access_token_key, access_token_secret):
    """Function for OAUTH Step 5.

    Finally open OAUTH-session.

    :param access_token_key:
    :param access_token_secret:
    :returns: auth_session
    :raises:
    """
    my_auth_session = OAuth1Session(
        config.OAUTH_KEY,
        config.OAUTH_SECRET,
        access_token=access_token_key,
        access_token_secret=access_token_secret,
    )

    return my_auth_session

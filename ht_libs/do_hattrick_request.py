from rauth import OAuth1Service
from rauth import OAuth1Session

from . import config



request_client = OAuth1Service(
           consumer_key = config.oauth_key,
           consumer_secret = config.oauth_secret,
           request_token_url = config.request_token_url,
           access_token_url = config.access_token_url,
           authorize_url = config.authorize_url,
           base_url = config.base_url,
           )



def fetch_authorize_url(oauth_url='oob', scope=''):
	#
	# Step 1 : Fetch Temporary Credential
	#
	request_token, request_token_secret = request_client.get_request_token(
			params={
				'oauth_callback': oauth_url,
				}
			) 

	#
	# Step 2 : Get the auth URL
	#
	authorize_url = request_client.get_authorize_url(
			request_token,
			scope=scope
			)

	return request_token, request_token_secret, authorize_url



def get_access_token(request_token, request_token_secret, auth_pin):
	#
	# Step 3 : Save auth_pin in var after the client was authorized
	# Step 4 : Exchange the request token for an access token
	#
	access_token_key, access_token_secret = request_client.get_access_token(
			request_token, request_token_secret, params={"oauth_verifier": auth_pin}
			)

	return access_token_key, access_token_secret



def open_auth_session(access_token_key, access_token_secret):
	#
	# Step 5 : Finally open oauth-session
	#
	my_auth_session = OAuth1Session(
						config.oauth_key,
                        config.oauth_secret,
                        access_token = access_token_key,
                        access_token_secret = access_token_secret,
                        )

	return my_auth_session

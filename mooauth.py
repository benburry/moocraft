#!/usr/bin/env python
#

'''
Requires:
  simplejson
  oauth
'''

__author__ = "Ben Burry <ben@burry.name>"
__version__ = "0.1"

import simplejson
import urllib2

try:
    import oauth.oauth as oauth
except ImportError:
    import oauth

REQUEST_TOKEN_URL = 'https://secure.moo.com/oauth/request_token.php'
ACCESS_TOKEN_URL = 'https://secure.moo.com/oauth/access_token.php'
AUTHORIZATION_URL = 'https://secure.moo.com/oauth/authorize.php'


class MooAuth():
    def __init__(self, consumer_key, consumer_secret, access_token=None):
        self._Consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self._signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self._access_token = access_token
        


    def _GetOpener(self):
        opener = urllib2.build_opener()
        return opener

    def _FetchUrl(self,
                    url,
                    post_data=None,
                    parameters=None):
        '''Fetch a URL, optionally caching for a specified time.

        Args:
          url: The URL to retrieve
          post_data:
            A dict of (str, unicode) key/value pairs.  If set, POST will be used.
          parameters:
            A dict whose key/value pairs should encoded and added
            to the query string. [OPTIONAL]

        Returns:
          A string containing the body of the response.
        '''
        # Build the extra parameters dict
        extra_params = {}
        if parameters:
          extra_params.update(parameters)

        # Add key/value parameters to the query string of the url
        #url = self._BuildUrl(url, extra_params=extra_params)

        if post_data:
            http_method = "POST"
            extra_params.update(post_data)
        else:
            http_method = "GET"

        req = self._makeOAuthRequest(url, parameters=extra_params,
                                                    http_method=http_method)
        self._signRequest(req, self._signature_method)


        # Get a url opener that can handle Oauth basic auth
        opener = self._GetOpener()

        #encoded_post_data = self._EncodePostData(post_data)

        if post_data:
            encoded_post_data = req.to_postdata()
            url = req.get_normalized_http_url()
        else:
            url = req.to_url()
            encoded_post_data = ""

        # Open and return the URL immediately if we're posting data
        if encoded_post_data:
          url_data = opener.open(url, encoded_post_data).read()
        else:
          url_data = opener.open(url).read()
        opener.close()

        # Always return the latest version
        return url_data

    def _makeOAuthRequest(self, url, token=None,
                                        parameters=None, http_method="GET"):
        '''Make a OAuth request from url and parameters

        Args:
          url: The Url to use for creating OAuth Request
          parameters:
             The URL parameters
          http_method:
             The HTTP method to use
        Returns:
          A OAauthRequest object
        '''
        if not token:
            token = self._access_token
        request = oauth.OAuthRequest.from_consumer_and_token(
                            self._Consumer, token=token,
                            http_url=url, parameters=parameters,
                            http_method=http_method)
        return request

    def _signRequest(self, req, signature_method=oauth.OAuthSignatureMethod_HMAC_SHA1()):
        '''Sign a request

        Reminder: Created this function so incase
        if I need to add anything to request before signing

        Args:
          req: The OAuth request created via _makeOAuthRequest
          signate_method:
             The oauth signature method to use
        '''
        req.sign_request(signature_method, self._Consumer, self._access_token)


    def getAuthorizationURL(self, token, url=AUTHORIZATION_URL):
        '''Create a signed authorization URL

        Returns:
          A signed OAuthRequest authorization URL
        '''
        req = self._makeOAuthRequest(url, token=token)
        self._signRequest(req)
        return req.to_url()

    def getAccessToken(self, url=ACCESS_TOKEN_URL):
        token = self._FetchUrl(url)
        return oauth.OAuthToken.from_string(token)

    def getRequestToken(self, url=REQUEST_TOKEN_URL):
        '''Get a Request Token 

        Returns:
          A OAuthToken object containing a request token
        '''
        resp = self._FetchUrl(url)
        token = oauth.OAuthToken.from_string(resp)
        return token
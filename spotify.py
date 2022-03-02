from contextlib import nullcontext
import sys
import base64
import requests
import datetime
import numpy as np
from urllib.parse import urlencode
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px


class SpotifyAPI(object):

    # class variables provided for you. Some need to be filled in:
    access_token = None
    access_token_expires = None
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = None

    # ------- TO DO -------
    # set client id and secret for all SpotifyAPI objects
    def __init__(self):
        return

    # ------- TO DO -------
    # @return the b64 encoded client id and secret
    def get_client_credentials(self):
        return

    # ------- TO DO -------
    # @return the formatted r request token header with b64 encoded credentials
    def get_token_headers(self):
        return

    # ------- TO DO -------
    # @return the token data (grant type)
    def get_token_data(self):
        return

    # ------- TO DO -------
    # @return True if able to perfrom authentication successfully
    def perform_auth(self):
        # 1. get token url, data and headers

        # 2. send post request to spotify
        r = requests.post()  # fill in the parameters for request

        # 3. check if request was successful

        # 4 set self.access token to access token from request
        self.access_token = None

        # 5. set expiration date dependencies
        self.access_token_expires = None
        self.access_token_did_expire = None
        return True

    # ------- TO DO -------
    # @return access token
    def get_access_token(self):

        # NOTE: Remember to check for if the token expired and if its not set yet
        return

    # ------- TO DO -------
    # @return request header for general requests
    def get_resource_header(self):
        return

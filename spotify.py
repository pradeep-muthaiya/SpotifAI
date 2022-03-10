import sys
import base64
import requests
import datetime
import numpy as np
from urllib.parse import urlencode
import plotly.express as px


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        print('client_creds:', client_creds)
        client_creds_b64 = base64.b64encode(client_creds.encode())
        print('client_creds_b64:', client_creds_b64)
        print('client_creds_b64_decode:', client_creds_b64.decode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        print('client_id:', self.client_id)
        print('client_secret', self.client_secret)
        token_url = self.token_url
        print('token_url:', token_url)
        token_data = self.get_token_data()
        print('token_data:', token_data)
        token_headers = self.get_token_headers()
        print('token_headers:', token_headers)
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    # ------ TO DO --------
    # @return the json of a track based on its id
    # NOTE: add parameters as needed!
    def get_resource_from_id(self):
        return

    # ------ TO DO --------
    # @return the json of an album based on its id
    def get_album(self, id_):
        return self.get_resource_from_id(of_type='albums', lookup_id=id_)

    # ------ TO DO --------
    # @return the json of an artist based on its id
    def get_artist(self, id_):
        return self.get_resource_from_id(of_type='artists', lookup_id=id_)

    # ------ TO DO --------
    # @return the json of a track based on its id
    def get_track(self, id_):
        return self.get_resource_from_id(of_type='tracks', lookup_id=id_)

    # ------ TO DO --------
    # @return the audio features of a track based on its id
    def get_features(self, id_):
        return

    # ------ TO DO --------
    # @return the json of a genre based on its id
    def get_genres(self, id_):
        return

    # ------ TO DO --------
    # @return the json of a playlist based on its id
    def get_playlist(self, id_):
        return

    # ------ TO DO --------
    # @return the row for a specific track with its features
    def get_df_row(self, track, of_type='search'):
        return

    # ------ TO DO --------
    # @return the json of a album based on its id
    def get_recommended_tracks(self, seed_artists, seed_genres, seed_tracks, limit):
        return

    # ------ OPTIONAL HELPER --------
    # @return the json of a album based on its id
    def base_search(self, query_params):
        return

    # ------ TO DO --------
    # @return the json of a search based on its query parameters
    def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
        return

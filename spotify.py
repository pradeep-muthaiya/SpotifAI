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

    def get_resource_from_id(self, lookup_id, of_type='artists', version='v1'):
        lookupurl = f"https://api.spotify.com/{version}/{of_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(lookupurl, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_album(self, id_):
        return self.get_resource_from_id(of_type='albums', lookup_id=id_)

    def get_artist(self, id_):
        return self.get_resource_from_id(of_type='artists', lookup_id=id_)

    def get_track(self, id_):
        return self.get_resource_from_id(of_type='tracks', lookup_id=id_)

    def get_features(self, id_):
        if isinstance(id_, list):
            return self.get_resource_from_id(of_type='audio-features', lookup_id=','.join(id_))
        return self.get_resource_from_id(of_type='audio-features', lookup_id=id_)

    def get_genres(self, id_):
        return self.get_artist(id_)['genres']

    def get_playlist(self, id_):
        return

    def get_df_row(self, track, of_type='search'):
        if of_type == 'id':
            track = self.get_track(track)
        # make df row
        row = [track['name'],
               track['id'],
               track['artists'][0]['name'],
               track['artists'][0]['id'],
               track['album']['name'],
               track['album']['id']]
        # get the song features
        features = self.get_features(track['id'])

        # combine together
        row.extend([value for value in features.values()][:11])
        row.extend([value for value in features.values()][16:])

        genres = self.get_genres(
            track['artists'][0]['id'])
        row.append(genres)
        return row

    def get_recommended_tracks(self, seed_artists, seed_genres, seed_tracks, limit):
        headers = self.get_resource_header()
        #query = {'seed_artists': seed_artists, 'seed_genres':seed_genres, 'seed_tracks':seed_tracks}
        endpoint = "https://api.spotify.com/v1/recommendations"

        #query = " ".join([f"{k}:{v}" for k,v in query.items()])
        query_params = urlencode(
            {"seed_artists": seed_artists, 'seed_genres': seed_genres, 'seed_tracks': seed_tracks})

        lookup_url = f"{endpoint}?{query_params}&limit={str(limit)}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}&limit=3"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            for key in list(query):
                if query[key] == '':
                    del query[key]
            query = " ".join([f"{k}:{v}" for k, v in query.items()])
        # if operator != None and operator_query != None:
        #    if operator.lower() == "or" or operator.lower() == "not":
        #        operator = operator.upper()
        #        if isinstance(operator_query, str):
        #            query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower()})
        return self.base_search(query_params)

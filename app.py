from dash.dependencies import Output, Input, State
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash
import sys
import spotify
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

with open(sys.argv[1]) as f:
    mylist = f.read().splitlines()

client_id = mylist[0]
client_secret = mylist[1]

spotify_API = spotify.SpotifyAPI(client_id, client_secret)


user_key = 'track'
# Setup table.
columns_input = ['track', 'artist', 'album', 'rating']
columns_store = ['Song', 'Song Id', 'Artist', 'Artist Id',
                 'Album', 'Album Id', 'danceability', 'energy',
                 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                 'instrumentalness', 'liveness', 'valence', 'tempo',
                 'duration_ms', 'time signature', 'genres', 'rating']
columns_display = ['Song', 'Song Id', 'Artist', 'Album', 'rating', 'danceability', 'energy',
                   'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                   'instrumentalness', 'liveness', 'valence', 'tempo',
                   'duration_ms', 'time signature']


table = dash_table.DataTable(
    columns=[{"name": column, "id": column} for column in columns_display], data=[], id="table",
    style_data={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'minWidth': '50px', 'width': '50px', 'maxWidth': '100px'
    }, style_table={
        'width': '100%'
    })

table2 = dash_table.DataTable(
    columns=[{"name": column, "id": column} for column in columns_display], data=[], id="table2",
    style_data={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'minWidth': '50px', 'width': '50px', 'maxWidth': '100px'
    }, style_table={
        'width': '100%'
    })

# Create app.
app = dash.Dash(prevent_initial_callbacks=True)
app.layout = html.Div([html.H1("SpotifAI")] + 
                      [dcc.Input(id=column, value=column) for column in columns_input] +
                      [html.Button("Save", id="save"), dcc.Store(id="cache", data=[]), dcc.Store(id='new_songs', data=[]),
                       dcc.Graph(id='display_avg'), table,
                       html.H2("Generate Songs"), html.Button(
                          "Generate", id="generate"), dcc.Input(id='gen_n', type='number', value=5),
                       html.Div(), table2])


# takes in the cache data and args from input and adds new song to cache data
@app.callback(Output("cache", "data"), [Input("save", "n_clicks")], [State("cache", "data")] +
              [State(column, "value") for column in columns_input])
def append(n_clicks, data, *args):

    # make the list of args into dictionary
    record = {columns_input[i]: arg for i, arg in enumerate(list(args))}

    # get rating value out of dict
    rating = record['rating']
    # delete rating value so dict can be used in query params for API call
    del record['rating']

    # delete the apostrophe in tracks as it messes with API calls
    for key in record:
        if "'" in record[key]:
            record[key] = record[key].replace("'", "")

    # call spotify API to search
    response = spotify_API.search(record, search_type="track")
    #print('response:', response)

    # if search fails:
    if response['tracks']['total'] == 0:
        return False

    # make df row
    row = spotify_API.get_df_row(response['tracks']['items'][0])
    row.append(int(rating))
    print('row:', row)

    # append new row to overall data
    data.append({columns_store[i]: arg for i, arg in enumerate(row)})
    # Return the updated data.
    return data

# updates table based on cache data


@app.callback(Output("table", "data"), Output("display_avg", "figure"), [Input("cache", "data")])
def updated_table(data):
    # print(data)
    temp_df = pd.DataFrame(data)
    temp_df = temp_df.drop(
        ['Artist Id', 'Album Id', 'genres'], axis=1)

    cols = ['danceability', 'energy', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence']

    means = []
    for i in cols:
        means.append(temp_df[i].mean())

    new_df = pd.DataFrame({'Features': cols, 'Average Value': means})
    fig = px.bar(new_df, x='Features', y='Average Value')
    return temp_df.to_dict('records'), fig


@app.callback(Output("table2", "data"), Output("new_songs", "data"), Input("generate", "n_clicks"),
              State("gen_n", "value"), State("cache", "data"), State("new_songs", "data"))
def generate_values(n_clicks, n, data, gen_data):
    # How to Generate New Tracks
    artists, genres, songs = [], [], []
    for i in data[:5]:
        artists.append(i['Artist Id'])
        genres.append(i['genres'])
        songs.append(i['Song Id'])

    # have to limit to 5 TOTAL seed values

    # EDIT CODE HERE ------
    artists = artists[:2]
    songs = songs[:1]

    if len(artists) > 1:
        artists = ','.join(artists)
    else:
        artists = artists[0]
    if len(genres) > 1:
        genres = [item for sublist in genres for item in sublist]
        genres = [genres[0]]
        if len(genres) > 1:
            genres = list(set(genres))
            genres = ','.join(genres)
        else:
            genres = genres[0]
    else:
        genres = genres[0]
    if len(songs) > 1:
        songs = ','.join(songs)
    else:
        songs = songs[0]

    print('artists:', artists)
    print('genres:', genres)
    print('songs:', songs)

    # Get recommended tracks json file
    response = spotify_API.get_recommended_tracks(
        artists, genres, songs, n)
    #print('response:', response)

    # END CODE EDITTING SECTION ----

    # find the values of each recommended track and add to gen_data
    for i in range(n):
        df_row = spotify_API.get_df_row(response['tracks'][i])
        gen_data.append(
            {columns_store[i]: arg for i, arg in enumerate(df_row)})

    # Machine Learning

    # EDIT CODE HERE -------
    df_train = pd.DataFrame(data)
    print('df_train:', df_train)
    X_train = df_train[['danceability', 'energy',
                        'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                        'instrumentalness', 'liveness', 'valence', 'tempo',
                        'duration_ms', 'time signature']]
    y_train = df_train[['rating']]

    print('X_train:', X_train)
    print('y_train:', y_train)

    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    print('coef:', regressor.coef_)

    print('gendata:', gen_data)
    df_fit = pd.DataFrame(gen_data)
    print('df_fit:', df_fit)

    df_fit_pred = df_fit[['danceability', 'energy',
                          'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                          'instrumentalness', 'liveness', 'valence', 'tempo',
                          'duration_ms', 'time signature']]
    print('df_fit2:', df_fit_pred)

    ratings = regressor.predict(df_fit_pred)
    print('ratings1:', ratings)

    # END CODE EDITING ---

    ratings = [item for sublist in ratings for item in sublist]
    print('ratings2:', ratings)

    df_fit['rating'] = ratings
    print('df_fit3:', df_fit)

    gen_data = df_fit.to_dict('records')
    print('gendata2:', gen_data)

    return gen_data, gen_data


if __name__ == '__main__':
    app.run_server()  # -*- coding: utf-8 -*-

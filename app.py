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

# open up id.txt for the client id and secret
with open(sys.argv[1]) as f:
    mylist = f.read().splitlines()

# assign the id and secret as variables
client_id = mylist[0]
client_secret = mylist[1]

# create our spotify_API instance
spotify_API = spotify.SpotifyAPI(client_id, client_secret)


user_key = 'track'
# Fill in what columns and values we want to take in from each set
columns_input = ['track', 'artist', 'album', 'rating']
columns_store = []
columns_display = []


table = dash_table.DataTable(
    columns=[{"name": column, "id": column} for column in columns_display], data=[], id="table")

table2 = dash_table.DataTable(
    columns=[{"name": column, "id": column} for column in columns_display], data=[], id="table2")

# Create dash app.
app = dash.Dash(prevent_initial_callbacks=True)

# Create the dash app layout. Add more values to the layout including titles, input states, input button, and then seperate input buttons for songs not included in the playlist
app.layout = html.Div([table, table2])


# takes in the cache data and args from input and adds new song to cache data
@app.callback(Output("table", "data"), [Input("save", "n_clicks")],
              [Input("table", "data")],
              [State(column, "value") for column in columns_input])
def append(save, data, *args):

    # take in inputs of given arguments, and current table data and search for song

    # from song get the features of the song

    # get data from the table

    # add the new information to the data

    # once its been added, send the data back to the table

    return


@app.callback(Output("table2", "data"), [Input("generate", "n_clicks")], [Input("table2", "data")],
              [Input("table1", "data")], [State(column, "value") for column in columns_input])
def generate_values(generate, data, data2, *args):

    # take in inputs of given arguments, and current table data and search for song

    # from song get the features of the song

    # get data from table1

    # using table data, and new song, perform ml using machinelearning.py

    # add the new information to table2

    # once its been added, send the data back to the table

    return


if __name__ == '__main__':
    app.run_server()  # -*- coding: utf-8 -*-

import webbrowser
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
from apps import commonmodules as cm
from apps import home
from apps.movies import movies_home, movie_profile
from apps.genres import genres_home, genre_profile


CONTENT_STYLE = {
    "margin-left": "1em",
    "margin-right": "1em", 
    "padding": "1em 1em"
}

app.layout = html.Div(
    [
        # Location Variable -- contains details about the url
        dcc.Location(id='url', refresh=True),
        cm.navbar,
        # Page Content -- Div that contains page layout
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)

@app.callback(
    [
         Output('page-content', 'children')
    ],
    [
        Input('url', 'pathname')
    ],
)

def displaypage(pathname):

    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    if eventid == 'url':
        if pathname in ['/', '/home']:
            returnlayout = home.layout
        elif pathname == '/movies':
            returnlayout = movies_home.layout
        elif pathname == '/movies/movie_profile':
            returnlayout = movie_profile.layout
        elif pathname == '/genres':
            returnlayout = genres_home.layout
        elif pathname == '/genres/genre_profile':
            returnlayout = genre_profile.layout
        else:
            returnlayout = 'error404'
    else:
        raise PreventUpdate
    
    return [returnlayout]

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)
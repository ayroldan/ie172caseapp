import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

layout = html.Div(
    [
        html.H2("Genres"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Genre Management")),
                dbc.CardBody(
                    [
                        dbc.Button('Add Genre', color="secondary", href='/genres/genre_profile'),
                        html.Hr(),
                        html.Div(
                            [
                                html.H6('Find Genres', style = {'fontWeight': 'bold'}),
                                dbc.Row(
                                    [
                                        dbc.Label("Search Genre", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="genre_name_filter", placeholder="Enter filter"
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    "This will contain the table for genres",
                                    id='genre_genrelist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
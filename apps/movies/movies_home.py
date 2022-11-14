import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2("Movies"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Movie Management")),
                dbc.CardBody(
                    [
                        dbc.Button('Add Movie', color="secondary", href='/movies/movie_profile?mode=add'),
                        html.Hr(),
                        html.Div(
                            [
                                html.H6('Find Movies', style = {'fontWeight': 'bold'}),
                                dbc.Row(
                                    [
                                        dbc.Label("Search Title", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="movie_name_filter", placeholder="Enter filter"
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    id='movie_movielist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    [
        Output('movie_movielist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('movie_name_filter', 'value')
    ]
)

def updatemovielist(pathname, searchterm):
    if pathname == '/movies':
        sql = """SELECT movie_name, genre_name, movie_id
                FROM movies m
                    INNER JOIN genres g ON m.genre_id = g.genre_id
                WHERE NOT movie_delete_ind"""
        val = []
        colnames = ['Movie Title', 'Genre', 'ID']

        if searchterm:
            sql += """ AND movie_name ILIKE %s"""
            val += [f"%{searchterm}%"]

        movies = db.querydatafromdatabase(sql, val, colnames)

        if movies.shape[0]:
            buttons = []
            for movieid in movies['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit/Delete', href=f"/movies/movie_profile?mode=edit&id={movieid}",
                                size="sm", color='warning'),
                        style={'text-align': 'center'}
                    )
                ]

            movies['Action'] = buttons

            movies.drop('ID', axis=1, inplace=True)
            
            table = dbc.Table.from_dataframe(movies,striped=True, bordered=True, hover=True, size='sm')
            return[table]

        else:
            return["There are no records that match the search term"]

    else:
        raise PreventUpdate

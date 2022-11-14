import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from urllib.parse import urlparse, parse_qs

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.Div(
            [
                dcc.Store(id='movieprof_toload', storage_type='memory', data=0)
            ]
        ),
        html.H2("Movies"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Title", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="movieprof_title", placeholder=""
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Release Date", width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='movieprof_releasedate',
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Genre", width=2),
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id='movieprof_genre',
                            clearable=True,
                            searchable=True,
                            options=[
                            ]
                        ),
                        className="dash-bootstrap"
                    ),
                    width=6
                )
            ],
            className="mb-3",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Wish to delete?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='movieprof_removerecord',
                            options=[ 
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1 }
                            ],
                            style={'fontWeight':'bold'},
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            id='movieprof_removerecord_div'
        ),
        html.Hr(),
        dbc.Button('Save', color="secondary", id='movieprof_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("", id='movieprof_feedback_header')),
                dbc.ModalBody("", id='movieprof_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="movieprof_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="movieprof_modal",
            is_open=False,
        ),
    ]
)



@app.callback(
    [
        Output('movieprof_genre', 'options'),
        Output('movieprof_toload', 'data'),
        Output('movieprof_removerecord_div', 'style')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def movieprof_loaddropdown(pathname, search):

    if pathname == '/movies/movie_profile':
        sql = """
            SELECT genre_name as label, genre_id as value
            FROM genres
            WHERE genre_delete_ind = False
        """
        values = []
        cols = ['label','value']
        df = db.querydatafromdatabase(sql, values, cols)
        genre_opts = df.to_dict('records')

        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]

        to_load = 1 if mode == 'edit' else 0
        removerecord_div = None if to_load else {'display': 'none'}
        

    else:
        raise PreventUpdate
    
    return [genre_opts, to_load, removerecord_div]



@app.callback(
    [
        Output("movieprof_modal", "is_open"),
        Output("movieprof_feedback_header", "children"),
        Output("movieprof_feedback_message", "children"),
        Output("movieprof_closebtn", "href")
    ],
    [
        Input("movieprof_submitbtn", "n_clicks"),
        Input("movieprof_closebtn", "n_clicks"),
    ],
    [
        State('movieprof_title', 'value'),
        State('movieprof_releasedate', 'date'),
        State('movieprof_genre', 'value'),
        State('url', 'search'),
        State('movieprof_removerecord', 'value')
    ]
)
def movieprof_submitprocess(submitbtn, closebtn,
                            
                            title, releasedate, genre,
                            search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid=ctx.triggered[0]['prop_id'].split(".")[0]
        openmodal = False
        feedbackheader = ''
        feedbackmessage = ''
        okay_href = None 
    else:
        raise PreventUpdate
    
    if eventid == 'movieprof_submitbtn' and submitbtn:
        openmodal = True

        inputs = [
            title,
            releasedate,
            genre
        ]

        if not all(inputs):
            feedbackheader = 'Saving Progress'
            feedbackmessage = "Please supply all inputs."
        
        elif len(title)>256:
            feedbackheader = 'Saving Progress'
            feedbackmessage = "Title is too long (length>256)."
        
        else:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':
                sqlcode = """INSERT INTO movies(
                    movie_name,
                    genre_id,
                    movie_release_date,
                    movie_delete_ind    
                )
                VALUES (%s, %s, %s, %s)
                """

                values = [title, genre, releasedate, False]
                db.modifydatabase(sqlcode, values)
                
                feedbackheader = 'Save Success'
                feedbackmessage = "Movie has been saved."
                okay_href = '/movies'
            
            elif mode == 'edit':
                parsed = urlparse(search)
                movieid = parse_qs(parsed.query)['id'][0]

                sqlcode = """UPDATE movies
                SET
                    movie_name = %s,
                    genre_id = %s,
                    movie_release_date = %s,
                    movie_delete_ind = %s
                WHERE
                    movie_id = %s
                """
                
                to_delete = bool(removerecord)

                values = [title, genre, releasedate, to_delete, movieid]
                db.modifydatabase(sqlcode, values)

                feedbackheader = 'Update Success'
                feedbackmessage = "Movie has been updated."
                okay_href = '/movies'

            else:
                raise PreventUpdate

    elif eventid == 'movieprof_closebtn' and closebtn:
        pass

    else:
        raise PreventUpdate
    
    return [openmodal, feedbackheader, feedbackmessage, okay_href]



@app.callback(
    [
        Output('movieprof_title', 'value'),
        Output('movieprof_releasedate', 'date'),
        Output('movieprof_genre', 'value'),
    ],
    [
        Input('movieprof_toload', 'modified_timestamp')
    ],
    [
        State('movieprof_toload', 'data'),
        State('url', 'search')
    ]
)
def loadmoviedetails(timestamp, to_load, search):
    if to_load == 1:
        sql = """SELECT movie_name, genre_id, movie_release_date
                FROM movies
                WHERE movie_id = %s"""
        
        parsed = urlparse(search)
        movieid = parse_qs(parsed.query)['id'][0]

        val = [movieid]
        colnames = ['title', 'genre', 'reldate']

        df = db.querydatafromdatabase(sql, val, colnames)

        title = df['title'][0]
        genre = df['genre'][0]
        reldate = df['reldate'][0]

        return [title, reldate, genre]

    else:
        raise PreventUpdate
        

@app.callback(
    [
        Output('movieprof_submitbtn', 'color'),
        Output('movieprof_submitbtn', 'children')
    ],
        Input('movieprof_removerecord', 'value')
)
def changebuttoncolor(removerecord):
    if bool(removerecord):
        color = 'danger'
        children = "Delete Record"

        return [color, children]

    else:
        color = 'secondary'
        children = "Submit"

        return [color, children]
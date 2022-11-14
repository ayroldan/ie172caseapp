import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2("Genres"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Name", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="genreprof_name", placeholder=""
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        html.Hr(),
        dbc.Button('Add Genre', color="secondary", id='genreprof_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("temp message", id='genreprof_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="genreprof_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="genreprof_modal",
            is_open=False,
        ),
    ]
)

@app.callback(
    [
        Output("genreprof_modal", "is_open"),
        Output("genreprof_feedback_message", "children"),
        Output("genreprof_closebtn", "href")
    ],
    [
        Input("genreprof_submitbtn", "n_clicks"),
        Input("genreprof_closebtn", "n_clicks"),
    ],
    [
        State('genreprof_name', 'value'),
    ]
)

def genreprof_submitprocess(submitbtn, closebtn, name):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid=ctx.triggered[0]['prop_id'].split(".")[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None 
    else:
        raise PreventUpdate
    
    if eventid == 'genreprof_submitbtn' and submitbtn:
        openmodal = True

        inputs = [
            name
        ]

        if not all(inputs):
            feedbackmessage = "Please supply all inputs."
        
        elif len(name)>256:
            feedbackmessage = "Genre name is too long (length>256)."
        
        else:
            sqlcode = """INSERT INTO genres(
                genre_name,
                genre_modified_on,
                genre_delete_ind    
            )
            VALUES (%s, %s, %s)
            """

            values = [name, datetime.now(), False]
            db.modifydatabase(sqlcode, values)
             
            feedbackmessage = "Genre has been saved."
            okay_href = '/genres'

    elif eventid == 'genreprof_closebtn' and closebtn:
        pass

    else:
        raise PreventUpdate
    
    return [openmodal, feedbackmessage, okay_href]

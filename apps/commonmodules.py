import webbrowser

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

navlink_style = {
    'color': '#fff',
    'margin-left': '15px',
} 

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row( 
                [
                    dbc.Col(dbc.NavbarBrand("IE 172 Case App", className = "m1-2"),
                    style = {'margin-left': '15px','margin-right': '25px'}
                    )
                ]
            ),
            href = '/home'
        ),
        dbc.NavLink("Home", href = "/home", style = navlink_style),
        dbc.NavLink("Movies", href="/movies", style=navlink_style),
        dbc.NavLink("Genres", href="/genres", style=navlink_style)
    ],
    dark=True,
    color='dark',
)
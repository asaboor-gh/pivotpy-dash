import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from app import app
from . import bands, dos, home, fermi, locpot
from dash.dependencies import Input, Output, State
#content = html.Div([
#    html.Div([html.H3('Pivotpy-Dash'),   
#    dbc.Tabs([
#        dbc.Tab(home.layout,label="Home"),
#        dbc.Tab(bands.layout,label="Bands"),
#        dbc.Tab(dos.layout,label="DOS"),
#        dbc.Tab(fermi.layout,label="Fermi Surface"),
#        dbc.Tab(locpot.layout,label="LOCPOT"),
#        dbc.Tab([
#            dbc.Checklist(
#            options=[
#                {"label": "Option 1", "value": 1}
#            ],
#            value=[],
#            id="switches-input",
#            switch=True,
#            ),
#        ],label="Switches"),
#    ],persistence=True)
#    ]),
#])
layout = html.Div([])

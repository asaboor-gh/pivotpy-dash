import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from time import time
import pivotpy as pp
from .bands import load_vasprun
from app import app
from dash.dash import no_update
from functools import lru_cache
from .re_usable import graph_config

@lru_cache(maxsize=2)
def get_plot(evr):
    return pp.plotly_dos_lines(evr)

layout = html.Div([
    html.H3('App 2'),
    dcc.Loading(className="loading",children=dcc.Graph(id='d1',config=graph_config))
])

@app.callback(Output('d1','figure'),[Input('dd','value')])
def return_2(value):

    print("App 2 Clicked with value {}".format(value))
    start = time()
    #evr = load_vasprun(value)
    fig = get_plot(value)
    print(time()-start)
    return fig
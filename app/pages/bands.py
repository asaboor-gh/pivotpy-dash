import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pivotpy as pp
from app import app
import time
import numpy as np 
from functools import lru_cache
from .re_usable import graph_config

@lru_cache(maxsize=2)
def load_vasprun(path):
    return pp.export_vasprun(path)

layout = html.Div([
    html.H3('App 1'),html.Div(id='d-out'),
    dcc.Loading(className="loading",children=dcc.Graph(id='d2',config=graph_config))
])

@app.callback(Output('d2','figure'),
              [Input('dd','value'),
               Input('red','value'),Input('green','value'),Input('blue','value')])
def return_1(file,v1,v2,v3):
    start = time.time()
    evr = load_vasprun(file)
    fields = np.array(evr.sys_info.fields)
    print(time.time()-start)
    l1 = '+'.join(fields[v1])
    l2 = '+'.join(fields[v2])
    l3 = '+'.join(fields[v3])
    return pp.plotly_rgb_lines(path_evr = evr,orbs=[v1,v2,v3],orblabels=[l1,l2,l3])

@app.callback(Output('d-out','children'),[Input('dd','value')])
def ddn(file):
    fields = pp.get_summary(pp.read_asxml(file)).fields #['s','pz']
    return html.Div([
        dcc.Dropdown(id = 'red',options=[{'label':l,'value':i} for i,l in enumerate(fields)],value=[0],multi=True,persistence=True,clearable=False),
        dcc.Dropdown(id = 'green',options=[{'label':l,'value':i} for i,l in enumerate(fields)],value=[1],multi=True,persistence=True,clearable=False),
        dcc.Dropdown(id = 'blue',options=[{'label':l,'value':i} for i,l in enumerate(fields)],value=[2],multi=True,persistence=True,clearable=False)
        ])
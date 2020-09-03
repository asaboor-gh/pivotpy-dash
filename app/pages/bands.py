import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
import time
import numpy as np 
import dash
from dash.dash import no_update
from .re_usable import graph_config
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from functools import lru_cache
import pivotpy as pp
import json

@lru_cache(maxsize=2)
def load_vasprun(path):
    return pp.export_vasprun(path)

@lru_cache(maxsize=2)
def get_figure(json_obj):
    if json_obj == None:
        raise PreventUpdate
    fig = json.loads(json_obj)
    fig['layout']['uirevision']=json_obj
    return fig

layout = html.Div([
    html.H3('App 1'),dcc.Loading(className='loading',children=html.Div(id='d-out')),
    html.Div([
        html.Button('Create Graph',n_clicks=0,id='click',className='btn-simple'),
        dcc.Loading(className='CenHeader',children=html.Div(id='hidden-div',hidden=True),type='dot')
    ],style={"display":"flex","padding":"20px 10px","align-items": "flex-end"}),
    dcc.Loading(className='loading',id='d-g',children=dcc.Graph(id='d2',config=graph_config))
])

@app.callback(Output('d-out','children'),[Input('dd','value')])
def ddn(file):
    fields = pp.get_summary(pp.read_asxml(file)).fields #['s','pz']
    return html.Div([
        dcc.Dropdown(id = 'red',options=[{'label':l,'value':i} for i,l in enumerate(fields)],value=[0],multi=True,persistence=True,clearable=False),
        dcc.Dropdown(id = 'green',options=[{'label':l,'value':i} for i,l in enumerate(fields)],value=[1],multi=True,persistence=True,clearable=False),
        dcc.Dropdown(id = 'blue',options=[{'label':l,'value':i} for i,l in enumerate(fields)],value=[2],multi=True,persistence=True,clearable=False)
        ])
    
@app.callback(Output('hidden-div','children'),
              [Input('dd','value'),
               Input('red','value'),Input('green','value'),Input('blue','value'),Input('click','n_clicks')],
              [State('hidden-div','children')])
def return_1(file,v1,v2,v3,clicks,child):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
        #raise PreventUpdate
        return child
    else:
        button_id = ctx.triggered[0]['prop_id']
        if(button_id in "click.n_clicks"):
            start = time.time()
            evr = load_vasprun(file)
            fields = np.array(evr.sys_info.fields)
            print(time.time()-start)
            l1 = '+'.join(fields[v1])
            l2 = '+'.join(fields[v2])
            l3 = '+'.join(fields[v3])
            fig = pp.plotly_rgb_lines(path_evr = evr,orbs=[v1,v2,v3],orblabels=[l1,l2,l3])
            return fig.to_json()

  
@app.callback(Output('d2','figure'),[Input('hidden-div','children')])
def render_graph(value):
    return get_figure(value)

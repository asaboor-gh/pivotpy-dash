import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from time import time
import pivotpy as pp
from .bands import load_vasprun
from app import app
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from dash.dash import no_update
from functools import lru_cache
from .re_usable import graph_config,lm_select,get_switch, load_vasprun, json_to_evr
import json
import numpy as np
 

layout = html.Div([
    html.Div([
        get_switch('run-dos','Load-Data'),
        dcc.Loading(className='CenHeader',children=html.Div(id='hidden-div-dos',hidden=True),type='dot')
    ],style={"display":"flex","padding":"20px 0px","align-items": "flex-start"}),
    lm_select(id='dos-lm'),
    get_switch('switch-graph-dos','Update Graph'),
    dcc.Loading(className='loading',children=dcc.Graph(id='dos-graph',config=graph_config))
])

@app.callback([Output('hidden-div-dos','children'),
               Output('dos-lm','options')],
              [Input('dd','value'),Input('run-dos','on')],
              [State('hidden-div-dos','children'),State('dos-lm','options')])
def return_dos(file,on,child,options):
    if not on:
        #raise PreventUpdate
        return (child,options)
    else:
        start = time()
        evr = load_vasprun(file)
        evr.pop('xml',None) # remove xml object
        json_str = json.dumps(evr,cls=pp.EncodeFromNumpy)
        fields = np.array(evr.sys_info.fields)
        print(time()-start)
        print('dos',evr.keys())
        if len(fields) != len(options):
            re_opts = [{'label':l,'value':i} for i,l in enumerate(fields)]
            return (json_str,re_opts)
        else:
            return (json_str,no_update)

@app.callback(Output('dos-graph','figure'),[Input('hidden-div-dos','children'),Input('switch-graph-dos','on'),Input('dos-lm','value')],[State('dos-graph','figure')])
def render_graph(value,on,lm,fig):
    if not on:
        raise PreventUpdate
    else:
        evr_to_graph = json_to_evr(value)
        fields = np.array(evr_to_graph.sys_info.fields)
        labels= fields[lm]
        return pp.plotly_dos_lines(evr_to_graph,orbs=lm,orblabels=labels)
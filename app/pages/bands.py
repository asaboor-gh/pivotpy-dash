import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
import time
import numpy as np 
import dash
from dash.dash import no_update
from .re_usable import graph_config, lm_select, get_switch, load_vasprun, json_to_evr, get_dbc_switch
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from functools import lru_cache
import pivotpy as pp
import json
import dash_daq as daq



layout = html.Div([
    html.Div([
        get_dbc_switch('run-calc','Load-Data'),
        dcc.Loading(className='CenHeader',children=html.Div(id='hidden-div',hidden=True),type='dot')
    ],style={"display":"flex","padding":"20px 0px","align-items": "flex-start"}),
    html.Div(id='d-out',children=[
        lm_select('red','Red Orbital(s)','red'),
        lm_select('green','Green Orbital(s)','green'),
        lm_select('blue','Blue Orbital(s)','blue')
        ],style={'display':'flex',"padding":"20px 10px","align-items": "flex-start"}),
    
    get_dbc_switch('switch-graph','Update Graph'),
    html.Div([
    dcc.Loading(className='loading',id='d-g',children=dcc.Graph(id='bands-graph',config=graph_config)),
    ],style={'height':'30vh','width':'50vw'})
])


    
@app.callback([Output('hidden-div','children'),
               Output('red','options'),Output('green','options'),Output('blue','options')],
              [Input('dd','value'),Input('run-calc','value')],
              [State('hidden-div','children'),State('red','options')])
def return_bands(file,on,child,options):
    if not on:
        #raise PreventUpdate
        return (child,options,options,options)
    else:
        start = time.time()
        evr = load_vasprun(file)
        evr.pop('xml',None) # remove xml object
        json_str = json.dumps(evr,cls=pp.EncodeFromNumpy)
        fields = np.array(evr.sys_info.fields)
        print(time.time()-start)
        print(evr.keys())
        if len(fields) != len(options):
            re_opts = [{'label':l,'value':i} for i,l in enumerate(fields)]
            return (json_str,re_opts,re_opts,re_opts)
        else:
            return (json_str,no_update,no_update,no_update)
            

  
@app.callback(Output('bands-graph','figure'),[Input('hidden-div','children'),Input('switch-graph','value')],[State('bands-graph','figure')])
def render_graph(value,on,fig):
    if not on:
        raise PreventUpdate
    else:
        evr_to_fig = json_to_evr(value)
        return pp.plotly_rgb_lines(evr_to_fig)

#Input('red','value'),Input('green','value'),Input('blue','value')
#l1 = '+'.join(fields[v1])
# l2 = '+'.join(fields[v2])
# l3 = '+'.join(fields[v3])
# fig = pp.plotly_rgb_lines(path_evr = evr,orbs=[v1,v2,v3],orblabels=[l1,l2,l3])
# return fig.to_json()
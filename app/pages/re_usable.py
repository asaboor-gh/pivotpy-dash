import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.exceptions import PreventUpdate
import json 
import pivotpy as pp
from functools import lru_cache

# Graph configuration.
graph_config = {'responsive':True,
                'editable':True,
                'toImageButtonOptions':{
                    'format':'svg',
                    'width':400,
                    'height':320
                    }
                }

# lm selection dropdown
def lm_select(id='lm',label='Select Orbitals',label_color='#1f2c56'):
    fields = ['s', 'py', 'pz', 'px', 'dxy', 'dyz', 'dz2', 'dxz', 'x2-y2']
    return html.Div([html.H6(label,style={'color':label_color}),
                    dcc.Dropdown(id = id,options=[
                     {'label':l,'value':i} for i,l in enumerate(fields)],
                     value=[0],multi=True,persistence=True,clearable=False)])

# Making a switch from checklist
def get_switch(id='my-switch',label='Select It',on=False):
    return html.Div([
        html.Div([daq.BooleanSwitch(id=id,on=on,color="#1f2c56",className='CenHeader')]),
        html.Div([html.H6(label,className='CenHeader',style={"padding":"0px 10px"})])
        ],style={"display":"inline-flex","padding":"20px 20px","align-items": "left"})
def get_dbc_switch(id='my-switch',label='Select It'):
    return dbc.Checklist(options=[{"label": label, "value": 1}],
            value=[],id=id,switch=True)

# Data functions
@lru_cache(maxsize=2)
def load_vasprun(path):
    return pp.export_vasprun(path)

@lru_cache(maxsize=2)
def json_to_evr(json_obj):
    if json_obj == None:
        raise PreventUpdate
    _out_evr =  json.loads(json_obj,cls=pp.DecodeToNumpy)
    return pp.Dict2Data(_out_evr)
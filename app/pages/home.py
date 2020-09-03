import numpy as np 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os,dash
from dash.dash import no_update
from app import app
import pivotpy as pp

input_ = dcc.Input(id='input_field',value=os.getcwd(),debounce=True,persistence=True)
include_ = dcc.Input(id = 'include_field',value=None,type="text",debounce=True,persistence=True)
exclude_ = dcc.Input(id = 'exclude_field',value=None,type="text",debounce=True,persistence=True)
selection_ = dcc.Dropdown(id='file_radio',options=[{'label':i,'value':i} for i in ['Files','Folders','Both']],value='Both',clearable=False,persistence=True)
depth_ = dcc.Dropdown(id='dirs_depth',options=[{'label':str(i),'value':i} for i in [1,2,3,4,5,'Max']],value=4,clearable=False,persistence=True)
intro_str = "Thank you for using Pivotpy-Dash!"

layout = html.Div([
    dcc.Markdown("""
                #### How to Proceed 
                On this page you can filter files/directories to work with. 
                Fill out below input and click on button at the end, 
                once you get a green success message, you are good to proceed through your project and switch between tabs.
                [Read More](https://github.com/massgh/pivotpy-dash/blob/master/README.md)
                 """),
    html.Div([
        html.H6("Litral Path to Project Folder"),
        input_
            ],className='main-folder'),
    html.Div([
        html.Div([html.H6("Include (e.g. xml,txt)"),include_],className='filters'),
        html.Div([html.H6("Exclude (e.g. py,js)"),exclude_],className='filters')
              ],className='flex-horizontal'),
    html.Div([
            html.Div([html.H6("Select Items Type"),selection_],className='filters'),
            html.Div([html.H6("Depth of Folders Tree"),depth_],className='filters'),
              ],className='flex-horizontal'),
    html.Div([
            html.Button("Apply Changes",id='submit',n_clicks=0,className='btn-simple'),
            html.Div(id='err-div',className="CenHeader",style={"color":"red"})
            ],style={"display":"flex","padding":"20px 10px","align-items": "flex-end"}),
    html.Div([html.Marquee(html.H6(intro_str,style={'color':'hotpink'}))])
    ],className='home-page')

@app.callback([Output('dd','options'),Output('err-div','children')],
              [Input('input_field','value'),
               Input('include_field','value'),
               Input('exclude_field','value'),
               Input('file_radio','value'),
               Input('dirs_depth','value'),
               Input('submit','n_clicks')])
def update_files(dir,in_,_exclude,_type,depth,click):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update,html.P('')
    else:
        button_id = ctx.triggered[0]['prop_id']
        if button_id in "submit.n_clicks":
            args=dict()
            if os.path.isdir(dir) == False:
                return no_update,html.P("ERROR: '{}' does not exist!".format(dir))
            elif os.path.isdir(dir):
                args.update({'path': dir})
            if _type in 'Files':
                args.update({'filesOnly': True})
            elif _type in 'Folders':
                args.update({'dirsOnly': True})
            if type(depth) == int:
                args.update({'depth': depth})
            
            ex_ = ['__pycache__','LICENSE','__init__.py','__main__.py']
            if _exclude != None:
                ex_.extend([v.strip() for v in _exclude.split(',')])
                args.update({'exclude':ex_})
            if in_ != None:
                in_ = [v.strip() for v in in_.split(',')]
                args.update({'include':in_})
        
            children, parent = pp.get_child_items(**args)
            labels = [child for child in children if not str(child).startswith('.')]
            values = [os.path.join(parent,child) for child in labels]
            options = [{'label': '{}'.format(label), 'value': value} for label,value in zip(labels,values)]
            return options,html.P('Successful!',style={"color":"green"})
        else:
            return no_update,html.P('')

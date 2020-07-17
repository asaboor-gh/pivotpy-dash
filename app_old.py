import dash
from dash.dependencies import Input,Output,State
import dash_core_components as dcc
import dash_html_components as html
import pivotpy as pp
import numpy as np
import os
import shutil
import json
import importlib as imp; #to reload module inside function
import plotly.graph_objs as go
import pivotpy.g_utils as sf
import PlotlyFile as pf
import variables
import InputFile
import pandas as pd

app = dash.Dash()


from components import sections


global prev_t,next_t;
prev_t=html.Button(id='prev-btn',n_clicks=0, className="prev",style={"position": "fixed", "left": "0px", "top": "0px"},children=u'\u2039') #u'\u2b9c'+
next_t=html.Button(id='next-btn',n_clicks=0,className="next",style={"position": "fixed", "right": "0px", "top": "0px"},children=u'\u203a') #u'\u2b9e'+

sections.append(prev_t)
sections.append(next_t)


app.layout = html.Div(className="wrap",style={"position": "absolute", "right": "50px","left":"50px","top":"60px","background":"whitesmoke"},children=sections)


if __name__ == '__main__':
    app.run_server(debug=False)



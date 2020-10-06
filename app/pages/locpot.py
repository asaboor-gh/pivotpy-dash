import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app


import pivotpy as pp 
import matplotlib.pyplot as plt
pp.quick_rgb_lines("E:/Research/graphene_example/ISPIN_1/bands/vasprun.xml",elim=[-9,9])
plot = pp.plt_to_html(dpi=1200,dash_html=True)
layout = html.Div(
    [
        dbc.Button(
            "Open Matplotlib",
            id="collapse-button",
            className="btn-simple",
            color="primary",
        ),
        dbc.Collapse([html.H3("Matplotlib Figure",className='card-title'),plot],
            id="collapse",
        ),
        html.Div(html.H6('After Collapse')),
        
    ]
)


@app.callback(
    [Output("collapse", "is_open"),Output("collapse-button","children")],
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open"),State("collapse-button","children")],
)
def toggle_collapse(n, is_open,child):
    if "Open" in child:
        label = "Close Matplotlib"
    else:
        label = "Open Matplotlib"
    if n:
        return not is_open,label
    return is_open,label
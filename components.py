# Import this in app.py
import dash_core_components as dcc
import dash_html_components as html
sections=[]

sections.append(html.Div(className='AppHeader',id="drop1",children=[
    html.Div(className='CenHeader',children=html.P('Directory')),
    dcc.Dropdown(className='CenHeader', id="drop1-1",persistence=True,options={'label':'Files','value' :1},
    value=0,clearable=False),
    html.Div(className='CenHeader',id="drop1-2",children=[html.P('1/N')])

]))
sections.append(html.Div(className="logo",style={"box-shadow":"none","border":"none","background":"none"},children=[html.H1('Pivotpy-Dash')]))
sections.append(html.Div(id='progressbar',children=html.Div(
style={"background":"#1f2c56","position":"fixed","width":"50vw","height":"4px","left":"0px","right":"0px","top":"0px","z-index":"99999"})))
sections.append(html.Div(id="dd-output-container"))
sections.append(html.Div(className="result_table",id='data_table'))
sections.append(html.Div(className='graphDiv',id = 'empty'))
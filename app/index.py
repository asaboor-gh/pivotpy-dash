import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sys,os
import pivotpy as pp
from app import app
from pages import bands, dos

path = os.getcwd()
items = pp.get_child_items(path=path,include=[],dirsOnly=True)
items_labels = items.children
items_values = [os.path.join(items.parent,child) for child in items.children]

#logo = html.Div(className="logo",style={"box-shadow":"none","border":"none","background":"none"},children=[html.H1('Pivotpy-Dash')])
navigation = html.Div(className='Navigation',children=[html.H1('Pivotpy-Dash')])

navigation.children.append(html.Div(style = {"display":"flex"},children=[
    dcc.Link(' Bands ', href='/pages/bands'), html.Br(), html.Br(),
    dcc.Link(' DOS ', href='/pages/dos')] 
))
header = html.Div(className='AppHeader',id="app-header",children=[])
header.children.append(html.Div(className='CenHeader',children=html.P('Directory')))
header.children.append(
   html.Div(id='page-content',children=dcc.Dropdown(id='dd',options=[
            {'label': '{}'.format(label), 'value': value} for label,value in zip(items_labels,items_values)
    ],clearable=False,persistence=True)) 
)
header.children.append(html.Div(className='CenHeader',id="drop1-2",children=[html.P('1/'+str(len(items.children)))]))


progressbar = html.Div(id='progressbar',children=html.Div(
style={"background":"#1f2c56","position":"fixed","width":str(1/len(items.children)*100)+"vw","height":"4px","left":"0px","right":"0px","top":"100px","z-index":"99999"}))

prev_t=html.Button(id='prev-btn',n_clicks=0, className="prev",style={"position": "fixed", "left": "0px", "top": "0px"},children=u'\u2039') #u'\u2b9c'+
next_t=html.Button(id='next-btn',n_clicks=0,className="next",style={"position": "fixed", "right": "0px", "top": "0px"},children=u'\u203a') #u'\u2b9e'+


app.layout = html.Div(style={"position": "absolute","top":"100px","left":"50px","right":"50px"},children=[
    dcc.Location(id='url', refresh=False),navigation,
    header, progressbar,prev_t,next_t,
    html.Div(id = 'display-page')
        ])


@app.callback(Output('display-page', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/bands':
        return bands.layout
    elif pathname == '/pages/dos':
        return dos.layout
    else:
        return ''
    
if len(sys.argv) > 1:
    port = sys.argv[1]
else:
    port = 8050
if __name__ == '__main__':
    app.run_server(debug=True,port=port)
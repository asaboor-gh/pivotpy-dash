import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import sys,os,dash
from dash.dash import no_update
import pivotpy as pp
from app import app
from pages import bands, dos, home, fermi, input, locpot
from pages.re_usable import graph_config
import dash_bootstrap_components as dbc

#path = os.getcwd()
#items = pp.get_child_items(path=path,include=[],dirsOnly=True)
#items_labels = items.children
#items_values = [os.path.join(items.parent,child) for child in items.children]
active_style   = {"color":  "#1f2c56","font-weight": "bold", "border-bottom": "3px solid  #1f2c56"}
inactive_style = {"float": "left","color": "blue", "text-align": "center",
  "padding": "0", "text-decoration": "none", "font-size": "1em",
  "box-shadow": "inset 0 -2px 0 0 #f9fdfcee"}
navigation = html.Div(className='Navigation',children=[html.H3('Pivotpy-Dash')])
menu_items = [
            html.Div([dcc.Link('Home',className='CenHeader', href='/pages/home')],id='home'),
            html.Div([dcc.Link('Bands',className='CenHeader', href='/pages/bands')],id='bands'),
            html.Div([dcc.Link('DOS',className='CenHeader', href='/pages/dos')],id='dos'),
            html.Div([dcc.Link('Fermi Surface',className='CenHeader', href='/pages/fermi')],id='fermi'),
            html.Div([dcc.Link('LOCPOT',className='CenHeader', href='/pages/locpot')],id='locpot'),
            html.Div([dcc.Link('Input',className='CenHeader', href='/pages/input')],id='input')
            ]
navigation.children.append(
    html.Div(
        [
    html.Div(
            menu_items,
        className='navbar')
        ])
    )
header = html.Div(className='AppHeader',id="app-header",children=[])
header.children.append(
    html.Div(className='CenHeader',children=html.H6('Path'))
    )
# This dropdown is updated through Home.

header.children.append(
   html.Div(id='page-content',children=[dcc.Dropdown(id='dd',clearable=False,persistence=True)]) 
    )
header.children.append(html.Div(className='CenHeader',id="counting",children=[html.H6('')]))


progressbar = html.Div(id='progressbar',className="progress",children=html.Div(
                        style={"width":"100vw","left":"0px","right":"0px"}
                        )
                    )

prev_t=html.Button(id='prev-btn',n_clicks=0, className="prev",style={"position": "fixed", "left": "0px", "top": "0px"},children=u'\u2039') #u'\u2b9c'+
next_t=html.Button(id='next-btn',n_clicks=0,className="next",style={"position": "fixed", "right": "0px", "top": "0px"},children=u'\u203a') #u'\u2b9e'+


app.layout = html.Div([
                        dcc.Location(id='url', refresh=False),navigation,
                        header,
                        progressbar,
                        prev_t,
                        next_t,
                        html.Div(id = 'display-page',className='content',children=[])
                    ])

# Changing values with button
@app.callback([Output('counting','children'),Output('progressbar','children')],
              [Input('dd','value'),Input('dd','options')])
def update_count(value,options):
    if options != None:
        values = [opt['value'] for opt in options]
        size = pp.get_file_size(value)
        return html.H6("{}: {}/{}".format(size,values.index(value)+1,len(options))), html.Div(
            style={"width":"{}vw".format((100*(values.index(value)+1))/len(options)),"left":"0px","right":"0px"})
    else:
        return no_update,no_update
    
# Changing directories
@app.callback(Output('dd','value'),
              [Input('next-btn', 'n_clicks'),Input('prev-btn', 'n_clicks'),Input('dd','options')],
              [State('dd','value')])
def update_file_index(next,prev,options,value):
    if options != None:
        values = [opt['value'] for opt in options]
        try:
            count_dir = values.index(value)
        except ValueError:
            count_dir = 0
        ctx = dash.callback_context
        if not ctx.triggered:
            button_id = 'No clicks yet'
            return no_update
        else:
            button_id = ctx.triggered[0]['prop_id']
            if(button_id in "next-btn.n_clicks"):
                count_dir = values.index(value)+1
                if(count_dir>len(values)-1):
                    count_dir=len(values)-1
            if(button_id in "prev-btn.n_clicks"):
                count_dir = values.index(value)-1
                if(count_dir<0):
                    count_dir=0
        return options[count_dir]['value']
    else:
        return no_update

#Serve pages
@app.callback([Output('display-page', 'children'),
               Output('home','style'),
               Output('bands','style'),
               Output('dos','style'),
               Output('fermi','style'),
               Output('locpot','style'),
               Output('input','style')],
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/home' or pathname == '/':
        return home.layout,active_style,inactive_style,inactive_style,inactive_style,inactive_style,inactive_style
    elif pathname == '/pages/bands':
        return bands.layout,inactive_style,active_style,inactive_style,inactive_style,inactive_style, inactive_style
    elif pathname == '/pages/dos':
        return dos.layout, inactive_style,inactive_style,active_style,inactive_style,inactive_style, inactive_style
    elif pathname == '/pages/fermi':
        return fermi.layout,inactive_style,inactive_style,inactive_style,active_style,inactive_style,inactive_style
    elif pathname == '/pages/locpot':
        return locpot.layout,inactive_style,inactive_style,inactive_style,inactive_style,active_style,inactive_style
    elif pathname == '/pages/input':
        return input.layout,inactive_style,inactive_style,inactive_style,inactive_style,inactive_style, active_style
    
if len(sys.argv) > 1:
    port = sys.argv[1]
else:
    port = 8050
    

#==========================
if __name__ == '__main__':
    app.run_server(debug=True,port=port)
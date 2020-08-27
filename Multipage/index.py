import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content',children=dcc.Dropdown(id='dd',options=[
            {'label': 'From Index Page - {}'.format(i), 'value': i} for i in [
                'PivotPy', 'PivotPy-Dash', 'Vasp2Visual'
            ]])),
    html.Div(id = 'display-page'),
    dcc.Link('Go to App 1 ', href='/apps/app1'), html.Br(), html.Br(),
    dcc.Link('Go to App 2 ', href='/apps/app2')
        ])


@app.callback(Output('display-page', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        return ''

if __name__ == '__main__':
    app.run_server(debug=True)
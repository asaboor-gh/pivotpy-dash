import dash

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = 'Pivotpy-Dash'
server = app.server
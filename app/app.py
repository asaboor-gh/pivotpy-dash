import dash
import dash_bootstrap_components as dbc
_metas=[{"name":"theme-color","content":"#1f2c56","name":"viewport", "content":"width=device-width, initial-scale=1"}]
app = dash.Dash(__name__, suppress_callback_exceptions=True,meta_tags=_metas)
app.title = 'Pivotpy-Dash'
server = app.server
import dash_html_components as html
import dash_bootstrap_components as dbc
layout = html.Div([html.H1('Upcoming Soon!'),
                   
        dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Active", active=True, href="#")),
        dbc.NavItem(dbc.NavLink("A link", href="#")),
        dbc.NavItem(dbc.NavLink("Another link", href="#")),
        dbc.NavItem(dbc.NavLink("Disabled", disabled=True, href="#")),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("Item 1"), dbc.DropdownMenuItem("Item 2")],
            label="Dropdown",
            nav=True,
        ),
    ],pills=True
)])
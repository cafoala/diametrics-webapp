import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.H1(),
        html.P(),
        html.Img(),
        html.Label(), 
        dcc.Dropdown(),
        html.Label(), 
        dcc.Dropdown(),
        html.Button()
    ]),
    html.Div([
        html.Div([
            dcc.Graph(),
            dcc.Graph()
        ]),
        html.Div([
            dcc.Graph(),
            html.Div([
                html.Label(), 
                daq.BooleanSwitch(),
                html.Label(),
                daq.BooleanSwitch(),
                html.Label(), 
                dcc.Slider(),
            ]),
        ])
    ])
])
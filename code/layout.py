import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="#")),
        dbc.NavItem(dbc.NavLink("How-to", href="#")),
        dbc.NavItem(dbc.NavLink("Theory and Code", href="#")),
        dbc.NavItem(dbc.NavLink("About Us", href="#")),
        ],
    brand="Diametrics",
    brand_href="#",
    color="dark",
    dark=True,
)
intro = html.Div(
    [
        html.H3('Welcome to', style={'textAlign': 'center'}),

        html.H1('Diametrics', style={'textAlign': 'center'}),

        html.P('A no-code webtool for calculating the metrics of glycemic control, creating visualisations and exploring continuous glucose monitoring (CGM) data',
                style={'textAlign': 'center'}
                ),
    ]
)

upload_section= html.Div([
        dbc.Row([
                dbc.Col(html.Div([
                    html.H2('Upload files'),
                    html.P('To begin, use the button below to select your CGM files'),
                    ]
                #style={'textAlign': 'left'}
                ), width=8),
                dbc.Col(dcc.Upload(dbc.Button('Select Files', color="secondary"),
                                multiple=True,
                                id='upload-data',))
        ]),
        dbc.Row([
                dbc.Col(html.Div(id='filelist'))
            ]),
    
       
    ],    
),


'''data_content = html.Div([
                    html.Div(
                    id='data-tbl',
                    style={
                        'width': '80%',
                        'height': '60px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    ),
])
metrics_content= html.Div([

        html.Div(
                id='metrics-tbl',
                style={
                    'width': '80%',
                    'height': '60px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
            ),
        ],
        ),'''

def create_layout():
    return html.Div([
    dcc.Store(storage_type='memory', id='raw-data-store'),
    dcc.Store(storage_type='memory', id='metrics-store'),
    dbc.Col(navbar),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([dbc.Col(dbc.Collapse(intro, id='intro-collapse', is_open=True))
                ]),
            dbc.Button("1. Upload files", color="primary", id="collapse-upload-button", n_clicks=0),
            dbc.Row([
                dbc.Col(
                    dbc.Collapse(
                        dbc.Card(upload_section, body=True),
                        id="upload-section-collapse",
                        is_open=True,
                    )
                ),
            ]),
            dbc.Row([
                dbc.Col(id='data-tbl'),
            ]),
            dbc.Row([
                dbc.Col(id='metrics-tbl'),
            ]),
            dbc.Row([
                dbc.Col(id='group-figs'),
            ]),
            dbc.Row([
                dbc.Col(id='individual-figs'),
            ]),
        ])
    )
])    
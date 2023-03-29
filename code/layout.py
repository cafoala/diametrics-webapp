import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import section_upload_content
import section_data_overview
import section_analysis_options
import section_metrics_tbl
import section_overview_figs
import section_individual_figs
import section_external_factors
import dash_player as dp
import instructions

image_path = 'assets/logo.png'

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
jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Welcome to Diametrics", className="display-3"),
            html.P(
                "A no-code webtool for Diabetes researchers to calculate the metrics of glycemic control and exploring continuous glucose monitoring (CGM) data",
                className="lead",
            ),
            html.Hr(className="my-2"),
            dbc.Row([
                dbc.Col([            
                    dp.DashPlayer(url='https://youtu.be/uUcuigkCrm0', controls=True, playing=True),
                ]),
                dbc.Col([
            dbc.Card([
                        dbc.CardHeader("You can use the Diametrics Dashboard to:"),
                        dbc.CardBody([
                            html.P(),
                            html.Ul([html.Li("Calculate the standard metrics of glycemic control"), 
                                    html.Li("Visualise your data"), 
                                    html.Li("Explore and calculate metrics for specific periods of interest")]),
                            html.Div([
                                "For step-by-step instructions and examples of how to use Diametrics, see the ", 
                                dcc.Link("documentation.", href='/documentation'),
                            ]),
                            html.Br(),
                            html.Div([
                                "To get started, ", 
                                dcc.Link("click here", href='/dashboard'),
                            ]),
                    ])])    
                ]),
                
                
            ]),
            html.Br(),
            dbc.Card([
                dbc.CardHeader('Created with support of'),
                dbc.CardBody([
                    dbc.Row([
    
                    dbc.Col(
                    html.Img(src='assets/exeter_logo.svg', width='180px')),
                    
                    dbc.Col(html.Img(src='assets/turing_logo.svg', width='180px')),

                    dbc.Col(html.Img(src='assets/extod_logo.svg', width='180px')),
                    ])
                ])], color="secondary") #, outline=True
             
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
)

instruction_section = instructions.layout

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "16rem",
    "margin-right": "2rem",
    "padding": "1.5rem 1rem",
}

sidebar = html.Div(
    [
        html.H3("Diametrics", className="display-6"),
        html.Hr(),
        html.Img(src=image_path),        
        html.P("Calculate the metrics of glycemic control",
            className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
                dbc.NavLink("Instructions", href="/page-2", active="exact"),
                dbc.NavLink("About Us", href="/page-3", active="exact"),
                dbc.NavLink("Contact", href="/contact", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    className="h-100 p-4 text-white bg-dark",
)

content = html.Div([
    dcc.Store(storage_type='memory', id='file-store'),
    dcc.Store(storage_type='memory', id='raw-data-store'),
    dcc.Store(storage_type='memory', id='processed-data-store'),
    dcc.Store(storage_type='memory', id='tir-store'),
    dcc.Store(storage_type='memory', id='poi-data-store'),
    dcc.Store(storage_type='memory', id='metrics-store'),
    dcc.Store(storage_type='memory', id='ranges-store'),
    dcc.Store(storage_type='memory', id='poi-store'),
    dcc.Store(storage_type='memory', id='poi-metrics-store'),
    #navbar,
    #intro,
    #jumbotron,
    #html.H1(['WebApp'], style={'textAlign':'center'}),
    #dbc.Card(
     #   dbc.CardBody([
    dbc.Tabs(
            [
                # Upload section
                dbc.Tab(
                    [dbc.Card(dbc.CardBody(
                        [section_upload_content.get_upload_layout()]),
                        style={'height':'75vh'},), #'overflowY': 'scroll', 
                        dbc.Row([
                            dbc.Col([                
                                dbc.Button('Next', id='upload-next-button', color='secondary', disabled=True)   
                            ], style={'text-align': 'right'})
                        ])],
                        label="1. Upload files", tab_id="upload-tab",
                        id='upload-tab', active_label_style={"color": "#FB79B3"}),
                # Data overview
                dbc.Tab(
                    [dbc.Card(dbc.CardBody(
                        [section_data_overview.get_datatable_layout()]),
                        style={'height':'75vh'}), #'overflowY': 'scroll',
                    dbc.Row([
                        dbc.Col([                
                            dbc.Button('Back', id='data-overview-back-button', color='secondary')
                        ]),
                        dbc.Col([                
                            dbc.Button('Next', id='data-overview-next-button', color='secondary', disabled=True)   

                        ], style={'text-align': 'right'})
                    ])], 
                        label="2. Check data", tab_id="data-tab",id="data-tab", 
                        disabled=True, active_label_style={"color": "#FB79B3"}),
                # Analysis options
                dbc.Tab(
                    [dbc.Card(dbc.CardBody(
                        [section_analysis_options.get_analysis_options_layout()]),
                        style={'height':'75vh','overflowY': 'scroll'}),
                    dbc.Row([
                        dbc.Col([                
                            dbc.Button('Back', id='analysis-options-back-button', color='secondary')
                        ]),
                        dbc.Col([                
                            dbc.Button('Next', id='analysis-options-next-button', color='secondary')   
                        ], style={'text-align': 'right'})
                    ])],
                        label="3. Analysis options", tab_id="other-metrics-tab", 
                        id='other-metrics-tab', disabled=True, 
                        active_label_style={"color": "#FB79B3"}),
                # Standard metrics
                dbc.Tab(
                    [dbc.Card(dbc.CardBody(
                        [section_metrics_tbl.get_metrics_layout()]),
                        style={'overflowY': 'scroll', 'height':'75vh'}),
                    dbc.Row([
                        dbc.Col([                
                            dbc.Button('Back', id='standard-metrics-back-button', 
                            color='secondary')   
                        ]),
                        dbc.Col([                
                            dbc.Button('Next', id='standard-metrics-next-button',
                            color='secondary', disabled=True)   
                        ], style={'text-align': 'right'})
                    ])],
                        label="4. Standard metrics", tab_id="metrics-tab", 
                        id='metrics-tab', disabled=True, 
                        active_label_style={"color": "#FB79B3"}),
                # Visualisatons
                dbc.Tab(
                    [dbc.Card(dbc.CardBody(
                        section_individual_figs.create_indiv_layout()),
                        style={'overflowY': 'scroll', 'height':'75vh'}),
                    dbc.Row([
                        dbc.Col([                
                            dbc.Button('Back', id='indiv-vis-back-button', color='secondary')   
                        ]),
                        dbc.Col([                
                            dbc.Button('Next', id='indiv-vis-next-button', color='secondary')   
                        ], style={'text-align': 'right'})
                    ])],
                        label="Visualisations", 
                        tab_id="indiv-vis", id='indiv-vis', disabled=True, 
                        active_label_style={"color": "#FB79B3"}),
                # PoI
                dbc.Tab(
                    [dbc.Card(
                        dbc.CardBody(
                            section_external_factors.create_period_of_interest()),
                            style={'overflowY': 'scroll', 'height':'75vh'}),
                    dbc.Row([
                        dbc.Col([                
                            dbc.Button('Back', id='poi-back-button', color='secondary')   
                        ]),
                    ])],
                        label="Advanced analysis", 
                        tab_id="external-tab", id='external-tab',
                        disabled=True, active_label_style={"color": "#FB79B3"}
                ),

            ],
            id="card-tabs",
            active_tab="upload-tab",
    ),
    
        #])
   # ),
])#, style=CONTENT_STYLE)



def create_tabs_layout():
    return html.Div([dcc.Location(id="url"), sidebar, content])
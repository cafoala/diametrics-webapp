import pandas as pd
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import datetime

def get_analysis_options_layout():
    accordion = html.Div(
        dbc.Accordion([
            dbc.AccordionItem([
                html.P('Edit the times below to adjust the wake/sleep period. The defaults are taken from the international consensus'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.H5('Day time'),
                            dbc.Row([
                                dbc.Col(width=3),
                                dbc.Col([html.Div(
                                    dmc.Group(
                                        spacing=50,
                                        children=[
                                            dmc.TimeInput(
                                                id='start-day-time', label="Start", format="24", value=datetime.datetime(year=1, month=1, day=1, hour=6, minute=0)
                                            ),
                                            dmc.TimeInput(
                                                id='end-day-time', label="End", format="24", value=datetime.datetime(year=1, month=1, day=1, hour=0, minute=0)
                                            ),
                                        ],
                                    ), style={'textAlign': 'center'})])]),
                        ]),
                    ], style={'textAlign': 'center'}),

                    dbc.Col([
                        dbc.Card([
                            html.H5('Night time', style={'textAlign': 'center'}), 
                            dbc.Row([
                                dbc.Col(width=3),
                                dbc.Col(html.Div(
                                    dmc.Group(
                                        spacing=50,
                                        children=[
                                            dmc.TimeInput(
                                                id='start-night-time', label="Start", format="24", value=datetime.datetime(year=1, month=1, day=1, hour=0, minute=0)
                                            ),
                                            dmc.TimeInput(
                                                id='end-night-time', label="End", format="24", value=datetime.datetime(year=1, month=1, day=1, hour=6, minute=0)
                                            ),
                                        ]
                                    ), style={'textAlign': 'center'}))])
                        ])
                    ]),
                ])
                ],
                title="Change the times for day and night",
            ),
            dbc.AccordionItem(
                [
                    html.Div(["Use the slider below to select threshold that you're interested in. \
                            This will be added to the standard thresholds for time in range, it \
                                won't replace them. To see the standard ranges see the ,",
                                "For step-by-step instructions and examples, see the ", 
                                dcc.Link("documentation.", href='/documentation'),            
                    ]),
                    #html.Div(id='tir-sliders'),
                    html.Div(id='tir-sliders'),
                    dbc.Button("Add another range", id='add-tir-slider', color='primary'),
                ],
                title="Adjust the percentage time in range thresholds",
            ),
            dbc.AccordionItem(
                [
                    html.P("Use the sliders below to select the thresholds for level 1 and level 2 hypoglycemic episodes"),

                    dbc.Row([
                        dbc.Col([
                            dbc.Card([dbc.CardBody([
                                html.H5('Length of events'),
                                dbc.Row([
                                    html.H6('Short events'),
                                    dbc.Col([
                                        dbc.Input(id='short-events-mins', type="number", min=0, max=1000, step=1,
                                             value=15)
                                    ], width=7),
                                    dbc.Col([
                                        html.P('mins')
                                    ])
                                ]),
                                dbc.Row([
                                    html.H6('Prolonged events'),
                                    dbc.Col([
                                        dbc.Input(id='prolonged-events-mins', type="number", min=0, max=1000, step=1,
                                            value=120),
                                    ], width=7),
                                    dbc.Col([
                                        html.P('mins')
                                    ])
                                ]),
                            ])
                            ])
                        ], width=3),
                               
                        dbc.Col([dbc.Card(dbc.CardBody([
                            html.H5('Hypoglycemia threshold (mmol/L)'),
                            html.H6('Level 1', style={'textAlign': 'right'}),
                            dcc.Slider(2.2, 22.2, step=0.1, value=3.9, 
                                        id='lv1-hypo-slider',
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        marks={
                                            2.2:{'label': 'Min.'},
                                            22.2:{'label': 'Max.'}
                                    }),

                            html.H6('Level 2', style={'textAlign': 'right'}),
                            dcc.Slider(2.2, 22.2, step=0.1, value=3.0,
                                        id='lv2-hypo-slider',
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        marks={
                                            2.2:{'label': 'Min.'},
                                            22.2:{'label': 'Max.'}
                                    })
                                ])),
                        ]),
                    
                        dbc.Col([dbc.Card(dbc.CardBody([
                                html.H5('Hyperglycemia threshold (mmol/L)',style={'textAlign': 'right'}),

                                html.H6('Level 1'),
                                dcc.Slider(2.2, 22.2, step=0.1, value=10.0, 
                                            id='lv1-hyper-slider',
                                            tooltip={"placement": "bottom", "always_visible": True},
                                            marks={
                                                2.2:{'label': 'Min.'},
                                                22.2:{'label': 'Max.'}
                                        }),

                                html.H6('Level 2'),
                                dcc.Slider(2.2, 22.2, step=0.1, value=13.9,
                                            id='lv2-hyper-slider',
                                            tooltip={"placement": "bottom", "always_visible": True},
                                            marks={
                                                2.2:{'label': 'Min.'},
                                                22.2:{'label': 'Max.'}
                                        })
                            ]))
                        ]),
                    ])
                ],
                title="Adjust the thresholds for glycemic events",
            ),    
dbc.AccordionItem(
                [
                    html.P("Use the sliders below to select the thresholds for level 1 and level 2 hypoglycemic episodes"),
                    dbc.Checklist(options=[{'label':'Remove LO/HI values', 'value':1},
                                        {'label':'Cap the glucose at selected cut-off','value':2}], 
                                        id='lo-hi-cutoff-checklist', value=[2]),
                    dbc.Row([
                        
                        dbc.Col([dbc.Card(dbc.CardBody([
                            html.H5('Low cut-off (mmol/L)'),
                            dcc.Slider(1.1, 5.3, step=0.1, value=2.1, 
                                        id='lo-cutoff-slider',
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        marks={1.1:{'label': '1.1'},
                                                5.3:{'label': '5.3'}}
                            )
                        ]))]),
                        dbc.Col([dbc.Card(dbc.CardBody([
                            html.H5('High cut-off (mmol/L)'),
                            dcc.Slider(19.0, 29.1, step=0.1, value=22.3,
                                        id='hi-cutoff-slider',
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        marks={19:{'label': '19.0'},
                                                29.1:{'label': '29.1'}}
                                       )
                                ])),
                        ]),
                    
                    ])
                ],
                title="Adjust the low/high glucose cut-off",
            ),    
        ],
        start_collapsed=True,
        )
    )
   
    analysis_layout = html.Div([
        dbc.Row([
                dbc.Col(#html.Div([
                    html.H2('Select your analysis options')),
                dbc.Col(
                    dbc.Alert(
                    [
                            html.I(className="bi bi-info-circle-fill me-2"),
                            'If you want to adjust the default analysis option do so by playing around with the buttons below',
                    ],
                    color="info",
                    className="d-flex align-items-center",
                    )),
                        ]),
           # ]),
        dbc.Row([
                dbc.Col(html.Div(accordion,id='options-accordion'))
            ]),
        
    ])
    return analysis_layout

def create_range_slider(n_clicks, children, units):
    id = 'tir-'+str(n_clicks)
    slider_id = id+'-slider'
    heading_id = id+'-heading'
    button_id = id+'-button'

    if units=='mmol/L':
        
        new_slider = html.Div([html.H6(id=heading_id),
                    dcc.RangeSlider(2.2, 22.2, step=0.1, value=[3.9, 7.8],
                                tooltip={"placement": "bottom", "always_visible": True},
                                marks={
                                        2.2:{'label': 'Min.'},
                                        22.2:{'label': 'Max.'}
                                },
                                id=slider_id
                            ),
        ])
    else:
        new_slider = dcc.RangeSlider(39, 399, step=1, value=[70, 180],
                                tooltip={"placement": "bottom", "always_visible": True},
                                marks={
                                        39:{'label': 'Min.'},
                                        399:{'label': 'Max.'}
                                },
                                id=slider_id
                            ),
    section = html.Div(dbc.Card([
                    html.H6(id=heading_id),
                    dbc.Row([
                        dbc.Col([
                            new_slider
                        ]),
                        dbc.Col([
                            dbc.Button('Remove', color="danger", id=button_id),
                        ], width=2)
                    ]),
                ]), id=id)
    if children is not None:
        children.append(section)
        return children
    else:
        return [section]         
        
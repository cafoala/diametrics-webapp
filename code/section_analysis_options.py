import pandas as pd
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import datetime


def get_analysis_options_layout():
    accordion = html.Div(
        dbc.Accordion([
            dbc.AccordionItem([
                        #html.P("Choose your units"),
                        dbc.RadioItems(
                            id="unit-type",
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": 'mmol/L', "value": 'mmol/L'},
                                {"label": "mg/dL", "value": 'mg/dL'},
                                #{"label": "Both", "value": 'both'},
                            ],
                            value='mmol/L',
                            style={'textAlign': 'center'}
                        ),
                    ],
                    title="Units",
                ),
            dbc.AccordionItem([
                html.P('Edit the times below to adjust the wake/sleep period. The defaults are taken from the international consensus'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.H5('Day time'),
                            html.Div(
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
                                ), style={'textAlign': 'center'}),
                        ]),
                    ],style={'text-align': 'center'}),

                    dbc.Col([
                        dbc.Card([
                            html.H5('Night time', style={'textAlign': 'center'}),
                            #create_range_slider(),
                            html.Div(
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
                                ), style={'textAlign': 'center'})
                        ])
                    ]),
                ])
                ],
                title="Day/night time",
            ),
            dbc.AccordionItem(
                [
                    html.P("Use the slider below to select threshold that you're interested in. \
                            This will be added to the standard thresholds for time in range, it \
                                won't replace them. To see the standard ranges see the THEORY SECTION"),
                    #html.Div(id='tir-sliders'),
                    html.Div(id='tir-sliders'),
                    dbc.Button("Add another threshold", id='add-tir-slider', color='primary'),
                ],
                title="Time in range thresholds",
            ),
            dbc.AccordionItem(
                [
                    html.P("Use the sliders below to select the thresholds for level 1 and level 2 hypoglycemic episodes"),
                    dbc.Row([
                        
                            dbc.Col([dbc.Card(dbc.CardBody([
                                html.H5('Hypoglycemia'),
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
                                html.H5('Hyperglycemia',style={'textAlign': 'right'}),

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
                title="Hypoglycemic episodes",
            ),
            
        ],
        start_collapsed=True,
        )
    )

   
    analysis_layout = html.Div([
        dbc.Row([
                dbc.Col(html.Div([
                    html.H2('Select your analysis options'),
                    html.P('If you want to adjust the default analysis option do so by playing around with the buttons below'),
                    ]
                #style={'textAlign': 'left'}
                )),
            ]),
        dbc.Row([
                dbc.Col(html.Div(accordion,id='options-accordion'))
            ]),
        dbc.Row([
                    dbc.Col([                
                        dbc.Button('Back', id='calculate-metrics-back-button', color='secondary')   
                    ]),
                    dbc.Col([                
                        dbc.Button('Next', id='calculate-metrics', color='secondary')   
                    ], style={'text-align': 'right'})
                ])
    ])
    return analysis_layout

def create_range_slider(n_clicks, children, units):
    id = 'tir-'+str(n_clicks)
    slider_id = id+'-slider'
    heading_id = id+'-heading'
    button_id = id+'-button'

    if units=='mmol/L':
        
        new_slider = html.Div([html.H6(id=heading_id),
                    dcc.RangeSlider(2.2, 22.2, step=0.1, value=[3.9, 10],
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
        
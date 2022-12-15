import pandas as pd
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc


def get_analysis_options_layout():
    accordion = html.Div(
        dbc.Accordion(
            [dbc.AccordionItem(
                    [
                        #html.P("Choose your units"),
                        dbc.RadioItems(
                            id="unit-type-options",
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": 'mmol/L', "value": 'mmol/L'},
                                {"label": "mg/dL", "value": 'mg/dL'},
                                {"label": "Both", "value": 'both'},
                            ],
                            value='mmol/L',
                            style={'textAlign': 'center'}
                        ),
                    ],
                    title="Units",
                ),
                dbc.AccordionItem(
                    [
                        html.P("Use the slider below to select threshold that you're interested in. This will be added to the standard thresholds for time in range, it won't replace them"),
                        #create_range_slider(),
                        html.Div(id='tir-sliders'),
                        html.Div(id='tir-slider-1'),
                        html.Div(id='tir-slider-2'),
                        html.Div(id='tir-slider-3'),
                        dbc.Button("Add another threshold", id='add-tir-slider', color='secondary'),
                    ],
                    title="Time in range thresholds",
                ),
                dbc.AccordionItem(
                    [
                        html.P("Use the sliders below to select the thresholds for level 1 and level 2 hypoglycemic episodes"),
                        dbc.Row([
                            
                                dbc.Col([dbc.Card(dbc.CardBody([
                                    html.H5('Hypoyglycemia'),
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
                                    html.H5('Hyperyglycemia',style={'textAlign': 'right'}),

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
                dbc.AccordionItem(
                    "Some kind of grouping shenanigans",
                    title="Grouping your data",
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
        dbc.Button('Calculate metrics', id='calculate-metrics', color='secondary')

    ])
    return analysis_layout

def create_range_slider(n_clicks, children, units):
        id = 'tir_slider_'+str(n_clicks)
        if units=='mmol/L':
            
            new_slider = html.Div([html.H4(id=id+'title'),
                        dcc.RangeSlider(2.2, 22.2, step=0.1, value=[3.9, 10],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    marks={
                                            2.2:{'label': 'Min.'},
                                            22.2:{'label': 'Max.'}
                                    },
                                    id=id
                                ),
            ])
        else:
            new_slider = dcc.RangeSlider(39, 399, step=1, value=[70, 180],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    marks={
                                            39:{'label': 'Min.'},
                                            399:{'label': 'Max.'}
                                    },
                                    id=id
                                ),
        if children is not None:
            children.append(new_slider[0])
        else:
            children = new_slider               
        return children
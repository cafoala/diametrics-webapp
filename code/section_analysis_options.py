import pandas as pd
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

def get_analysis_options_layout():
    accordion = html.Div(
        dbc.Accordion(
            [dbc.AccordionItem(
                    [
                        html.P("Choose your units"),
                        dcc.RadioItems(
                            ['mmol/L', 'mg/dL', 'Both'],
                            value='mmol/L ',
                            id='unit-type-options',
                            inline=True
    )
                        
                    ],
                    title="Units",
                ),
                dbc.AccordionItem(
                    [
                        html.P("Use the slider below to select threshold that you're interested in. This will be added to the standard thresholds for time in range, it won't replace them"),
                        #create_range_slider(),
                        dcc.RangeSlider(2.2, 22.2, step=0.1, value=[3.9, 10],
                                tooltip={"placement": "bottom", "always_visible": True},
                                marks={
                                        2.2:{'label': 'Min.'},
                                        22.2:{'label': 'Max.'}
                                }
                            ),
                        dbc.Button("Add another threshold", color='secondary'),
                    ],
                    title="Time in range thresholds",
                ),
                dbc.AccordionItem(
                    [
                        html.P("Use the sliders below to select the thresholds for level 1 and level 2 hypoglycemic episodes"),
                        html.H4('Level 1 threshold'),
                        dcc.Slider(2.2, 22.2, step=0.1, value=3.9, 
                                    id='lv1-hypo-slider',
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    marks={
                                        2.2:{'label': 'Min.'},
                                        22.2:{'label': 'Max.'}
                                }),
                        html.H4('Level 2 threshold'),
                        dcc.Slider(2.2, 22.2, step=0.1, value=3.0,
                                    id='lv2-hypo-slider',
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    marks={
                                        2.2:{'label': 'Min.'},
                                        22.2:{'label': 'Max.'}
                                })
                    ],
                    title="Hypoglycemic episodes",
                ),
                dbc.AccordionItem(
                    "This is the content of the third section",
                    title="Grouping your data",
                ),
                dbc.AccordionItem(
                    "This is the content of the third section",
                    title="Period of interest",
                ),
            ],
        )
    )

   

    analysis_layout = html.Div([
        dbc.Row([
                dbc.Col(html.Div([
                    html.H2('Select your analysis options'),
                    html.P('If you want to adjust the default thresholds do so by playing around with the buttons below'),
                    ]
                #style={'textAlign': 'left'}
                )),
            ]),
        dbc.Row([
                dbc.Col(html.Div(accordion,id='options-accordion'))
            ]),
        dbc.Row([
            dbc.Col(html.Div(accordion,id='options-accordion'))
        ]),

    ])
    return analysis_layout

def create_range_slider(units):#n_clicks):
    #id = 'tir_slider_'+str(n_clicks)

    dcc.RangeSlider(2.2, 22.2, value=[3.9, 10], step=0.1, tooltip={"placement": "bottom", "always_visible": True})
    return 

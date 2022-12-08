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
                            ['mmol/L', 'mg/dL'],#, 'Both'],
                            value='mmol/L ',
                            id='unit-type-options',
                            inline=True)
                    ],
                    title="Units",
                ),
                dbc.AccordionItem(
                    [
                        html.P("Use the slider below to select threshold that you're interested in. This will be added to the standard thresholds for time in range, it won't replace them"),
                        #create_range_slider(),
                        html.Div(id='tir-sliders'),
                        dbc.Button("Add another threshold", id='add-tir-slider', color='secondary'),
                    ],
                    title="Time in range thresholds",
                ),
                dbc.AccordionItem(
                    [
                        html.P("Use the sliders below to select the thresholds for level 1 and level 2 hypoglycemic episodes"),
                        html.H5('Level 1'),
                        dcc.Slider(2.2, 22.2, step=0.1, value=3.9, 
                                    id='lv1-hypo-slider',
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    marks={
                                        2.2:{'label': 'Min.'},
                                        22.2:{'label': 'Max.'}
                                }),
                        html.H5('Level 2'),
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
                dbc.AccordionItem(create_period_of_interest(),
                    id='poi-section',
                    title="Period of interest",
                ),
            ],
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
            new_slider = dcc.RangeSlider(2.2, 22.2, step=0.1, value=[3.9, 10],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    marks={
                                            2.2:{'label': 'Min.'},
                                            22.2:{'label': 'Max.'}
                                    },
                                    id=id
                                ),
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

def create_period_of_interest():
    
    poi_template = pd.DataFrame([['ID must match your IDs in the webapp',	'dd/mm/yy/ HH:MM',	'dd/mm/yy/ HH:MM',	'This can be used to label repeating periods']], columns= ['ID', 'startDateTime', 'endDateTime', 'label'])
    return html.Div([
        html.P('This section enables you to take a more in depth look at different periods of interest in your data. \
            For this to work you\'ll need to upload a file that includes the ID of the participant, the start and end times of the period \
            of interest and an optional label. From there, you\'ll get a breakdown of the metrics of glycemic control\
            for all of the periods you\'ve entered.\
            For this part you need to pay close attention to the instruction because there\'s lots of ways to mess this up. Good luck brave warrior.'),
       
        dbc.Row([
            dbc.Col([html.H5('Instructions'),
                html.P('1. Create an excel or csv file with headers shown in the template below or download the template using the export button'),
                    html.P('2. Fill in the IDs, must match with the ones in your processed data (table in above section)'),
                    html.P('3. The start and end time of the period must be in the format DD/MM/YY HH:MM'),
                    html.P('4. Add a label if you\'d like to'),
                    html.P('5 Add an optional set period to look at the window after your period of interest'),
            ]),
            dbc.Col([html.H5('File template'),
                    dash_table.DataTable(data=poi_template.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in poi_template.columns],
                                export_format="csv",
                                export_headers="display",
                                style_table={'overflowX': 'auto',},
                                style_cell={'whiteSpace': 'normal',},),
                    dcc.Upload(dbc.Button('Upload periods file', color="secondary"),
                                multiple=False,
                                id='upload-poi-data',),
            ], width=5),
        html.Div(id='poi-datafile'),
        html.H5('Time after period'),
        dcc.Checklist(['1 hour', '2 hours', '3 hours', '4 hours'], id='time-after-checklist', inline=False),

    ])
])
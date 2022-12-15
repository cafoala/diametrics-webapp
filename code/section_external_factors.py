import pandas as pd
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

poi_template = pd.DataFrame([['ID must match your IDs in the webapp',	'dd/mm/yy/ HH:MM',	'dd/mm/yy/ HH:MM',	'This can be used to label repeating periods']], columns= ['ID', 'startDateTime', 'endDateTime', 'label'])
accordion = dbc.Accordion(
            [dbc.AccordionItem(
                    [
                        html.P("This section will be for diet")
                    ],
                    title="Diet",
                ),
                dbc.AccordionItem(
                    [
                        html.P("This section will be for insulin data")
                    ],
                    title="Insulin",
                ),
                dbc.AccordionItem(
                    [
                        html.P("This section will be for exercise")
                    ],
                    title="Exercise",
                ),
                dbc.AccordionItem(
                    [html.H5('File template'),
                    dash_table.DataTable(data=poi_template.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in poi_template.columns],
                                export_format="csv",
                                export_headers="display",
                                style_table={'overflowX': 'auto',},
                                style_cell={'whiteSpace': 'normal',},),
                    dcc.Upload(dbc.Button('Upload periods file', color="secondary"),
                                multiple=False,
                                id='upload-poi-data',),
                    html.Div(id='poi-datafile'),
                    html.H5('Time after period'),
                    dcc.Checklist(['1 hour', '2 hours', '3 hours', '4 hours'], id='time-after-checklist', inline=False),
                                ],
                    title="Other",
                ),
])

def create_period_of_interest():
    return html.Div([
        html.H2('Incorporating external factors'),
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
        ]),
        dbc.Row(accordion)
])
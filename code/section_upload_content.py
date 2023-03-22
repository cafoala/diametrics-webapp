from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_uploader as du
import pandas as pd


def get_upload_layout():
        return html.Div([
        dbc.Row([
                dbc.Col(
                        html.H2('Upload files'), width=4),
                dbc.Col(dbc.Alert(
                        [
                                html.I(className="bi bi-info-circle-fill me-2"),
                                'Your CGM files must match the company format and be in xls, csv or txt',
                        ],
                        color="info",
                        className="d-flex align-items-center",
                ))]), 
        dbc.Row([
                #dbc.Col(width=2),
                dbc.Col([dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select CGM Files here'),
                                ]),
                                style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=True
                        ),
                        #html.Br(),
                        html.Div(id='filelist'),
                ], width=8),
                dbc.Col([dbc.Card(dbc.CardBody([
                        html.H5('Options', style={'textAlign':'center'}),
                        html.H6('Device'),
                        html.Div(
                                dbc.RadioItems(
                                        id="device-button",
                                        class_name="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary",
                                        labelCheckedClassName="active",
                                        options=[
                                                {"label": "Libre", "value": 'FreeStyle Libre'},
                                                {"label": "Dexcom", "value": 'Dexcom'},
                                                {"label": "Medtronic", "value": 'Medtronic', 'disabled':True},
                                        ],
                                        value='FreeStyle Libre',
                                ), className="radio-group"
                        ),
                        html.Br(),
                        html.H6('Units'),
                        html.Div(
                                dbc.RadioItems(
                                        id="units-first-button",
                                        class_name="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary",
                                        labelCheckedClassName="active",
                                        options=[
                                                {"label": "mmol/L", "value": 'mmol/L'},
                                                {"label": "mg/dL", "value": 'mg/dL'},
                                        ],
                                        value='mmol/L',
                                ), className="radio-group"
                        ),         
                        html.Br(),             
                        html.H6('Date format'),
                        html.Div([
                                dbc.RadioItems(
                                        id="datetime-format",
                                        class_name="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary",
                                        labelCheckedClassName="active",
                                        options=[
                                                {"label": "European", "value": 'euro'},
                                                {"label": "American", "value": 'amer'},
                                        ],
                                        value='euro',
                                )
                        ], className="radio-group"),
                        
                ]))]) #, width=4
        ]),
        
        ])

def create_file_list(list_of_names):
        data = pd.DataFrame(list_of_names)
        data.columns = ['Selected files:']
        return html.Div([
            #html.H5(''),
            html.Br(),
            html.Div(dash_table.DataTable(data=data.to_dict('records'),
                style_table={
                        'overflowX': 'auto',
                        'maxHeight': '25vh',
                },
                style_header={
                        'backgroundColor': 'rgb(210, 210, 210)',
                        'color': 'black',
                        'fontWeight': 'bold',
                        'textAlign':'left'
                },
                style_cell={
                            'whiteSpace': 'normal',
                            'font-family':'sans-serif',
                            'textAlign':'center'
                },
                ), style={'textAlign': 'center'}), 
            html.Br(),
            html.P('If you\'re happy with these files, click next to process your data'), #, style={'text-align':'right'}
            ])
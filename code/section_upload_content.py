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
                                'To begin, use the button to select the CGM files you want to work with. If you want to start again with your upload just the box again and reselect.',
                        ],
                        color="info",
                        className="d-flex align-items-center",
                ))]),
        html.Br(),
        dbc.Row([dbc.Col(width=2),
                dbc.Col([
                        html.Div(du.Upload(text='Drag and drop or click to select files', 
                                max_files=1000, id='dash-uploader', 
                                text_completed='Upload file complete: ')),
                        dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
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
                        ]),
                
                dbc.Col(width=2),
                ]),
        html.Div(id='filelist'),
        ])

def create_file_list(list_of_names):
        data = pd.DataFrame(list_of_names)
        data.columns = ['Selected files:']
        return html.Div([
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
                        html.H6('Select the format of the date in your files:'),
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
                        ),
                        html.Br(),
                        html.P('If you\'re happy with these files, click next to process your data'), #, style={'text-align':'right'}
            ])
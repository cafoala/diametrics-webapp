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
                                'To begin, use the button to select the CGM files you want to work with',
                        ],
                        color="info",
                        className="d-flex align-items-center",
                ))]),

                dbc.Row([dbc.Col(width=2),
                        dbc.Col(html.Div(du.Upload(text='Drag and drop or click to select files', 
                                        max_files=1000, id='dash-uploader', 
                                        text_completed='Upload file complete: '))),
                        dbc.Col(width=2),
                        ]),
                html.Div(id='filelist'),
                html.Div(id='callback-output')
        ])

def create_file_list(list_of_names):
        data = pd.DataFrame(list_of_names)
        data.columns = ['Selected files:']
        return html.Div([
            #html.H5(''),
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
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

def get_upload_layout():
        return dbc.Card(
                        dbc.CardBody([
                                dbc.Row([
                                        dbc.Col(html.Div([
                                        html.H2('Upload files'),
                                        html.P('To begin, use the button to select your CGM files'),
                                        ]
                                        #style={'textAlign': 'left'}
                                        ), width=8),
                                        dbc.Col(dcc.Upload(dbc.Button('Select Files', color="secondary"),
                                                        multiple=True,
                                                        id='upload-data',))
                                ]),
                                dbc.Row([
                                        dbc.Col(html.Div(id='filelist'))
                                ]),
                        ]),
        )
def create_file_list(list_of_names):
    return html.Div([
            html.H5('Selected files:'),
            html.Div([i +' ' for i in list_of_names], 
            style={"overflow": "scroll",
                    'width': '80%',
                    'height': '100px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'justify': "center",}),
            html.P('If you\'re happy with these files, click the button below to process your data'),
            dbc.Button('Preprocess data', id='preprocess-button', color='secondary'),
            ])
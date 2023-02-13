from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_uploader as du
import pandas as pd

def get_upload_layout():
        return dbc.Card(dbc.CardBody([
                dbc.Row([
                        dbc.Col([
                                html.H2('Upload files'),
                                html.P('To begin, use the button to select your CGM files'),
                                dcc.Upload(
                                        id='upload-data',
                                        children=html.Div([
                                        'Drag and Drop or ',
                                        html.A('Select Files')
                                        ]),
                                        style={
                                        'width': '80%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px'
                                        },
                                        # Allow multiple files to be uploaded
                                        multiple=True),
                        ],width=8 ),
                #]),
                #dbc.Row([
                        dbc.Col(id='filelist', width=3)
                ]),
        ]))

def create_file_list(list_of_names):
        data = pd.DataFrame(list_of_names)
        data.columns = ['Selected files:']
        return html.Div([
            #html.H5(''),
            html.Div(dash_table.DataTable(data=data.to_dict('records'),
                style_table={
                        'overflowX': 'auto',
                        'height': 250,
                        #'width':200
                        },
                #style_data_conditional=[
                 #       {
                  #      'if': {'row_index': 'odd'},
                   #     'backgroundColor': 'rgb(220, 220, 220)',
                    #    }
                #],
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
                ), style={'borderWidth': '1px'}), 
            #html.P('If you\'re happy with these files, click next to process your data'),
            #dbc.Row(dbc.Col([dbc.Button('Next', id='preprocess-button', color='secondary')], style={'text-align': 'right'})),
            ])
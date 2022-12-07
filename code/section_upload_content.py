from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc


def create_file_list(list_of_names):
    return html.Div([
            html.H5('Selected files:'),
            html.Div([i for i in list_of_names], 
            style={"overflow": "scroll",
                    'width': '70%',
                    'height': '100px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'justify': "center",}),
            html.P('If you\'re happy with these files, click the button below to process your data'),
            dbc.Button('Preprocess data', id='preprocess-button', color='secondary', n_clicks=0)
            ])
import base64
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import io
import preprocessing

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), header=None)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded), header=None)

        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+', header=None)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing file with name: ' + filename
        ])
    return preprocessing.preprocess_df(df, filename)

def get_datatable_layout():
    return html.Div([
                html.H2('Data details'),

                html.Div(dbc.Spinner(spinner_style={"width": "3rem", "height": "3rem"}), id='data-tbl-div'), 
            ])

def create_data_table(children):
    data_details = pd.DataFrame.from_dict(children)[['Filename', 'ID', 'Usable', 'Device', 'Interval', 'Data Sufficiency', 'Start Time', 'End Time']]
    
    return html.Div([
                #html.H2('Data details'),

        dash_table.DataTable(
                    id='data-tbl',
                    columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                                if i == "iso_alpha3" or i == "Filename" or i == "id"
                                else {"name": i, "id": i, "hideable": True, "selectable": True}
                                for i in data_details.columns
                    ],
                    data=data_details.to_dict('records'),
                    style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                #'width':'200px'
                            },
                    
                    style_table={
                        'overflowX': 'auto',
                        'height': 300,
                        },
                    editable=True,              # allow editing of data inside all cells
                    filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                    sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                    export_format="csv",
                    export_headers="display",
                    ),
                    html.P('The table shows your preprocessed data. Please make sure to check that the data is \
                        what you want for your files and edit accordingly. Most importantly, the ID, the start and \
                            end dates as these will be used for the rest of your data analysis. If you do edit, \
                              please press the reprocess button to get an updated table'),
                    dbc.Button('Choose analysis options', id='analysis-options-button', color='secondary')    
            ])
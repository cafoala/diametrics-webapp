import base64
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import io
import preprocessing
import metrics_helper

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
            df = pd.read_table(
                io.StringIO(decoded.decode('utf-8'))) # , delimiter = r'\s+', header=None

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing file with name: ' + filename
        ])
    return preprocessing.preprocess_df(df, filename)

def get_datatable_layout():
    return html.Div([
                html.H2('Data overview'),
                html.Div(dbc.Spinner(spinner_style={"width": "3rem", "height": "3rem"}), id='data-tbl-div'),
                html.P('The table shows your preprocessed data. Please make sure to check that the data is \
                        what you want for your files. You can edit the IDs'),
                dbc.Row([
                    dbc.Col([                
                        dbc.Button('Back', id='analysis-options-back-button', color='secondary')   
                    ]),
                    dbc.Col([                
                        dbc.Button('Next', id='analysis-options-button', color='secondary')   
                    ], style={'text-align': 'right'})
                ])
            ])

def create_data_table(children):
    data_details = pd.DataFrame.from_dict(children)[['Filename', 'Usable', 'ID', 'Start DateTime', 'End DateTime', 'Days', 'Data Sufficiency']] #'Device', 'Interval', 'Units',
    data_details.columns = ['Filename', 'Usable', 'ID', 'Start DateTime', 'End DateTime', 'Days', 'Data Sufficiency (%)'] #'Interval (mins)', 'Units',
    data_details['Usable'] = data_details['Usable'].replace({True:'Yes', False:'No'})
    return html.Div([
                #html.H2('Data details'),

        dash_table.DataTable(
                    id='data-tbl',
                    columns=[
                                {"name": i, "id": i, "deletable": False, "editable": True, "selectable": True}
                                if i == "ID" or i == "Start DateTime" or i == "End DateTime"
                                else {"name": i, "id": i, "editable": False, "selectable": False}
                                for i in data_details.columns
                    ],
                    data=data_details.to_dict('records'),
                    style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                #'width':'200px'
                            },
                    style_cell={
                            'whiteSpace': 'normal',
                },
                    style_table={
                        'overflowX': 'auto',
                        'height': 250,
                        },
                    #editable=True,              # allow editing of data inside all cells
                    #filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                    #sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                    #export_format="csv",
                    #export_headers="display",
                    #fixed_rows={'headers':True},
                    tooltip_header={
                        'Data Sufficiency (%)': 'The percentage of available CGM readings divided by the number of readings that should be present',
                        'Usable': 'Whether or not the CGM data can be used by the program (True/False)',
                        'Units': 'mmol/L or mg/dL',
                        'ID': 'How you will identify your CGM files, it comes from the filename',
                        'Start DateTime': 'The first reading from your CGM data (YYYY-MM-DD HH:MM:SS)',
                        'End DateTime': 'The last reading from your CGM data (YYYY-MM-DD HH:MM:SS)'
                    },
                    ), 
            ])

def calculate_data_sufficiency(filename, start, end, raw_data):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    subject = [i for i in raw_data if i['Filename']==filename][0]
    interval = subject['Interval']
    data = pd.DataFrame(subject['data'])
    data['time'] = pd.to_datetime(data['time'])
    results = metrics_helper.helper_missing(data, interval, start, end)
    ds = results['Data Sufficiency']
    return ds

def merge_glc_data(table_data, raw_data):
    results = pd.DataFrame()
    for row in table_data:
        if row['Days'] == 'NA':
            continue
        subject = [i for i in raw_data if i['Filename']==row['Filename']][0]
        data = pd.DataFrame(subject['data'])
        start = row['Start DateTime']
        end = row['End DateTime']
        data_sub = data.loc[(data['time']>=start)&(data['time']<=end)]
        if subject['Units']=='mg/dL':
            data_sub['glc'] = data_sub['glc']*0.0557
        data_sub['ID'] = row['ID']
        data_sub = data_sub#.to_dict('records')
        results = results.append(data_sub)

    results = results.to_dict('records')
    return results


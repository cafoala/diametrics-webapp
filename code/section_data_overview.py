import base64
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import io
import preprocessing
import metrics_helper
from datetime import timedelta

def get_datatable_layout():
    return html.Div([
        dbc.Row([dbc.Col(
                    html.H2('Data overview'), 
                width=4),
                dbc.Col(
                    dbc.Alert(
                    [
                            html.I(className="bi bi-info-circle-fill me-2"),
                            'The table below will show an overview of your data. You can edit the IDs and the start and end time',
                    ],
                    color="info",
                    className="d-flex align-items-center",
                    )
                )
            ]),
        html.Div(dbc.Spinner(spinner_style={"width": "3rem", "height": "3rem"}),
                    style={'textAlign':'center'}, id='data-tbl-div'),
            ])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), header=None, names = [i for i in range(0, 20)])
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded), header=None, names = [i for i in range(0, 20)])
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_table(
                io.StringIO(decoded.decode('utf-8')), header=None, names = [i for i in range(0, 20)])

    except Exception as e:
        print(e)
        data_dictionary = {'Usable': False, 'Filename': filename, 
            'Device':'N/A', #'Interval': 'N/A', 'data': 'N/A',
            'ID': 'N/A', 'Start DateTime': 'N/A', 'End DateTime': 'N/A',
            'Days': 'N/A', 'Data Sufficiency (%)':'N/A'}
        return data_dictionary
    return preprocessing.preprocess_df(df, filename)

def read_files(files):
    processed_files = []
    for file in files:
        filename = file.name
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(file, header=None, names = [i for i in range(0, 20)])
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(file, header=None, names = [i for i in range(0, 20)])
            elif 'txt' or 'tsv' in filename:
                # Assume that the user upl, delimiter = r'\s+'oaded an excel file
                df = pd.read_table(file, header=None, names = [i for i in range(0, 20)])
            processed_files.append(preprocessing.preprocess_df(df, filename))

        except Exception as e:
            data_dictionary = {'Usable': False, 'Filename': filename, 
             #'Device':'N/A', #'Interval': 'N/A', 'data': 'N/A',
                'ID': 'N/A', 'Start DateTime': 'N/A', 'End DateTime': 'N/A',
                'Days': 'N/A', 'Data Sufficiency (%)':'N/A'}
            processed_files.append(data_dictionary)
    return processed_files

def read_files_2(file, filename, dt_format, device, units):
    content_type, content_string = file.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), header=None, names = [i for i in range(0, 30)])
            df.columns = df.iloc[0]
            df = df.iloc[1:]
            df = df.reset_index(drop=True)

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))#, header=None, names = [i for i in range(0, 20)])
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_table(
                io.StringIO(decoded.decode('utf-8')))# header=None, ,names = [i for i in range(0, 40)
        
        return preprocessing.preprocess_df(df, filename, dt_format, device, units)

    except Exception as e:
        data_dictionary = {'Usable': False, 'Filename': filename, 
         #'Device':device, #'Interval': 'N/A', 'data': 'N/A',
            'ID': 'N/A', 'Start DateTime': 'N/A', 'End DateTime': 'N/A',
            'Days': 'N/A', 'Data Sufficiency (%)':'N/A'}
        return data_dictionary

def create_data_table(children):
    data_details = pd.DataFrame.from_dict(children)
    data_details = data_details[['Filename', 'Usable', 'Device', 'ID', 'Start DateTime', 'End DateTime', 'Days', 'Data Sufficiency (%)']] #'Device', 'Interval', 'Units',
    data_details['Usable'] = data_details['Usable'].replace({True:'Yes', False:'No'})

    #days = data_details['Days'].apply(lambda x: x.split(' ')[0]).replace({'N/A':0}).astype(int)
    #index = days[days<14].index

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
                            'font-family':'sans-serif',
                            'textAlign':'center',
                            'backgroundColor':'white'
                    },
                    style_table={
                        'overflowX': 'auto',
                        'maxHeight': '50vh',
                        },
                    
                    style_header={
                        'backgroundColor': 'rgb(210, 210, 210)',
                        'color': 'black',
                        #'fontWeight': 'bold'
                    },
                    editable=True,              # allow editing of data inside all cells
                    #filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                    sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                    #export_format="csv",
                    #export_headers="display",
                    #fixed_rows={'headers':True},
                    tooltip_header={
                        'Data Sufficiency (%)': 'The percentage of readings present. Highlighted orange if less than 70% (see FAQs)',
                        'Usable': 'Whether or not the CGM data can be used by the program (True/False)',
                        'Units': 'mmol/L or mg/dL',
                        'ID': 'How you will identify your CGM files, it comes from the filename',
                        'Start DateTime': 'The first reading from your CGM data (YYYY-MM-DD HH:MM:SS)',
                        'End DateTime': 'The last reading from your CGM data (YYYY-MM-DD HH:MM:SS)',
                        'Days': 'Number of days of data for each file. Will be highlighted orange if less than 14 days (see FAQs)'
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
    ds = results['Data Sufficiency (%)']
    return ds

def merge_glc_data(table_data, raw_data, interp, interp_method, interp_limit):
    results = pd.DataFrame()
    for row in table_data:
        if row['Days'] == 'N/A':
            continue
        subject = [i for i in raw_data if i['Filename']==row['Filename']][0]
        data = pd.DataFrame(subject['data'])
        data['time'] = pd.to_datetime(data['time'])
        start = row['Start DateTime']
        end = row['End DateTime']
        data_sub = data.loc[(data['time']>=start)&(data['time']<=end)]
        
        ### CHECK THIS! ### 
        if subject['Units']=='mg/dL':
            data_sub['glc'] = pd.to_numeric(data_sub['glc'])/18
        if interp:
            data_sub = metrics_helper.interpolate(data_sub, subject['Interval'], interp_method, interp_limit)
        
        data_sub['ID'] = row['ID']
        
        results = results.append(data_sub)
    results = results.to_dict('records')
    return results

def create_conditional_formatting(rows):
    df = pd.DataFrame(rows)
    days_series = df['Days'].apply(lambda x: x.split(' ')[0]).replace({'N/A':0}).astype(int)
    index = days_series[days_series<14].index
    style_conds = [
                        {
                            'if': {
                                'column_id': 'Days',
                                'row_index': index,
                            },
                            'backgroundColor': 'rgb(253, 205, 172)',
                        },

                        {
                            'if': {
                                'column_id': 'Data Sufficiency (%)',
                                'filter_query': '{Data Sufficiency (%)} < 70'
                            },
                            'backgroundColor': 'rgb(253, 205, 172)',
                        },
                        {
                            'if': {
                                'filter_query': '{{Usable}} = {}'.format('No'),
                                'filter_query': '{{Days}} = {}'.format('N/A'),
                            },
                            'column_id': 'Usable',
                            'backgroundColor': 'tomato',
                            'color': 'white'
                        },
                    ]
    return style_conds
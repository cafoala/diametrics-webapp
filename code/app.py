import base64
import datetime
import io
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import logging
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_uploader as du
import preprocessing
import metrics_experiment
import periods
from dash.exceptions import PreventUpdate
import layout_helper
#from preprocess_data_dash import *
logging.basicConfig(level=logging.DEBUG)

external_stylesheets = [dbc.themes.JOURNAL]
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#, suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="#")),
        dbc.NavItem(dbc.NavLink("How-to", href="#")),
        dbc.NavItem(dbc.NavLink("Theory and Code", href="#")),
        dbc.NavItem(dbc.NavLink("About Us", href="#")),
        ],
    brand="Diametrics",
    brand_href="#",
    color="dark",
    dark=True,
)
intro = html.Div(
    [
        html.H3('Welcome to', style={'textAlign': 'center'}),

        html.H1('Diametrics', style={'textAlign': 'center'}),

        html.P('A no-code webtool for calculating the metrics of glycemic control, creating visualisations and exploring continuous glucose monitoring (CGM) data',
                style={'textAlign': 'center'}
                ),
    ]
)

upload_section= html.Div([
        dbc.Row([
                dbc.Col(html.Div([
                    html.H2('Upload files'),
                    html.P('To begin, use the button below to select your CGM files'),
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
    
       
    ],    
),


data_content = html.Div([
                    html.Div(
                    id='data-tbl',
                    style={
                        'width': '80%',
                        'height': '60px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    ),
])
metrics_content= html.Div([

        html.Div(
                id='metrics-tbl',
                style={
                    'width': '80%',
                    'height': '60px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
            ),
        ],
        ),
    
app.layout = html.Div([
    dcc.Store(storage_type='local', id='raw-data-store'),
    dcc.Store(storage_type='local', id='metrics-store'),
    dbc.Col(navbar),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([dbc.Col(dbc.Collapse(intro, id='intro-collapse', is_open=True))
                ]),
            dbc.Button("1. Upload files", color="primary", id="collapse-upload-button", n_clicks=0),
            dbc.Row([
                dbc.Col(
                    dbc.Collapse(
                        dbc.Card(upload_section, body=True),
                        id="upload-section-collapse",
                        is_open=True,
                    )
                ),
            ]),
            dbc.Row([
                dbc.Col(id='data-tbl'),
            ]),
            dbc.Row([
                dbc.Col(id='metrics-tbl'),
            ]),
            dbc.Row([dbc.Col(html.Div([
                html.H2('IS ANYONE THERE!??!'),
                html.Div(id='test-table-main')]))
            ]),

            dbc.Row([
                dbc.Col(id='group-figs'),
            ]),
            dbc.Row([
                dbc.Col(id='individual-figs'),
            ]),
        ])
    )
])

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


# Collapse data table options panel once calculated
@app.callback(Output("upload-section-collapse", "is_open"),
    Input("collapse-upload-button", "n_clicks"), 
    Input('preprocess-button', 'n_clicks'),
    State("upload-section-collapse", "is_open"),
    prevent_initial_call=True)
def collapse_upload(n_toggle, n_metrics, is_open):
    if n_toggle or n_metrics:
        return not is_open# , not is_open]
    return is_open

# Collapse data table options panel once calculated
@app.callback(Output('data-tbl-collapse', 'is_open'),
    Input("collapse-data-tbl-button", "n_clicks"), 
    Input('calculate-metrics', 'n_clicks'),
    State("data-tbl-collapse", "is_open"),
    prevent_initial_call=True)
def collapse_datatbl(n_toggle, n_metrics, is_open):
    if n_toggle or n_metrics:
        return not is_open# , not is_open]
    return is_open#, is_open]
    
# Collapse options panel once calculated
@app.callback(Output('intro-collapse', 'is_open'),
    Input('preprocess-button', 'n_clicks'),
    prevent_intitital_call=True
)
def toggle_right_options(n_clicks):
    if n_clicks:
        return False


# List the filenames
@app.callback(Output('filelist', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
    prevent_initial_call=True)
def list_files(list_of_contents, list_of_names):
    if list_of_contents is not None:

        file_list = html.Div([
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
        return file_list#, False
                
@app.callback([Output('raw-data-store', 'data'),
    Output('data-tbl', 'children')],
    Input('preprocess-button', 'n_clicks'),
    State('upload-data', 'last_modified'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True)
def preprocess_data(n_clicks, list_of_dates, list_of_contents, list_of_names):
    #if n_clicks is not None:
    #    n_clicks = 0
    if n_clicks is None or list_of_dates is None:
        raise PreventUpdate
    if n_clicks >0:
        print('preprocessing')
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        
        data_details = pd.DataFrame.from_dict(children)[['Filename', 'ID', 'Usable', 'Device', 'Interval', 'Data Sufficiency', 'Start Time', 'End Time']]
        data_table = html.Div([
                html.H2('Data details'),

                dash_table.DataTable(
                    id='data_tbl',
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
                        #'height': 300,
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
                    dbc.Button('Calculate metrics', id='calculate-metrics', color='secondary')
            ]),
            
        collapse_table = html.Div([
                dbc.Button("2. Check your data", color="primary", id="collapse-data-tbl-button", n_clicks=0),
                dbc.Row([
                    dbc.Collapse(
                        dbc.Card(data_table, body=True),
                        id="data-tbl-collapse",
                        is_open=True,
                    )
            ]),
        ])
        return (children, collapse_table)


# Create metrics table
@app.callback([Output('metrics-store', 'data'),
        Output('metrics-tbl', 'children')],
        Input('calculate-metrics', 'n_clicks'),
        State('raw-data-store', 'data'),
        prevent_initial_call=True)
def calculate_metrics(n_clicks, raw_data):
    if n_clicks is None or raw_data is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate
    all_results = []
    #day_results = []
    #night_results = []

    for i in raw_data:
        if i['Usable']==True:
            df_id = pd.DataFrame.from_dict(i['data'])
            df_id.time = pd.to_datetime(df_id.time)
            logging.debug(df_id.head())
            # Total df
            all = metrics_experiment.calculate_all_metrics(df_id, ID=i['ID'], unit=i['Units'], interval=i['Interval'])
            all['period'] = 'All'
            all_results.append(all)

            # Breakdown df into night and day
            df_day, df_night = periods.get_day_night_breakdown(df_id)
            
            # Daytime breakdown metrics 
            day= metrics_experiment.calculate_all_metrics(df_day, ID=i['ID'], unit=i['Units'], interval=i['Interval'])
            day['period'] = 'Day'
            #day_results.append(day)
            all_results.append(day)

            
            # Night breakdown metrics
            night= metrics_experiment.calculate_all_metrics(df_night, ID=i['ID'], unit=i['Units'], interval=i['Interval'])
            night['period'] = 'Night'
            #night_results.append(night)
            all_results.append(night)
    metrics = pd.DataFrame.from_dict(all_results).round(2) # this is stupid - already a dict
    units = dcc.RadioItems(
                ['mmol/L', 'mg/dL'],
                'mmol/L ',
                id='unit-type',
                inline=True
            ),
    time_period = dcc.RadioItems(
                ['All', 'Day', 'Night'],
                'All',
                id='period-type',
                inline=True
            )
    graph1 = html.Div([
        dcc.Dropdown(
                metrics.columns.unique(),
                'Average glucose',
                id='xaxis-column'
        ),
        dcc.Graph(
                    id='example-graph1',
                    figure=px.bar(metrics, x='ID', y='Average glucose')
        )
    ])

    graph2 = html.Div([
        dcc.Dropdown(
                metrics.columns.unique(),
                'eA1c',
                id='xaxis-column'
            ),
        dcc.Graph(
                id='example-graph2',
                figure=px.box(metrics, y='eA1c')#, y='Average glucose')
    )
    ])

    graph3 = html.Div([

        #html.Div([
         #   dcc.Dropdown(
          #      metrics['ID'].unique(),
           #     metrics['ID'].unique()[0],
            #    id='xaxis-column'
            #),
            
        #], style={'width': '48%', 'display': 'inline-block'}),
            dcc.Dropdown(
                metrics['ID'].unique(),
                metrics['ID'].unique()[0],
                id='xaxis-column'
            ),
            dcc.Graph(
                        id='example-graph3',
                        figure=px.line(raw_data[0]['data'], x='time', y='glc')
            )
    ])
    
    metrics_layout = html.Div([
        dbc.Row([
                    dbc.Col(html.H2('Metrics of Glycemic Control')),
                    dbc.Col(units),
                    dbc.Col(time_period),
        ]),
        dbc.Row([
                dbc.Col(id='test-table',)# width=8),
                #dbc.Col([metrics_table], width=8),
                #dbc.Col(graph2),

                ],
                className="g-0",),
        '''dbc.Row([
            dbc.Col(graph1, width=5),
            dbc.Col(graph3),
        ])'''
    ])
    collapse_table = html.Div([
            dbc.Button('3. Metrics'),                 
            dbc.Row([
                    dbc.Collapse(
                        dbc.Card(metrics_layout),
                        id="metrics-tbl-collapse",
                        is_open=True,
                    )
            ]),
        ])
    #metrics.to_dict('records')
    return all_results, collapse_table #metrics_table # data_table, 


@app.callback(
    Output('test-table', 'children'),
    #Input('unit-type', 'value'),
    Input('period-type', 'value'),
    State('metrics-store', 'data')
    )
def update_metrics_table(period, metrics_data):
    print(period)
    df = pd.DataFrame.from_dict(metrics_data)
    sub_df = df[df['period']==period].round(2)
    metrics_table = layout_helper.create_metrics_table(sub_df)
    #print(metrics_table.head())
    return metrics_table




@app.callback(Output('output-div', 'children'),
              Input('submit-button','n_clicks'),
              State('stored-data','data'),
              State('xaxis-data','value'),
              State('yaxis-data', 'value'))
def make_graphs(n, data, x_data, y_data):
    if n is None:
        return dash.no_update
    else:
        bar_fig = px.bar(data, x=x_data, y=y_data)
        # print(data)
        return dcc.Graph(figure=bar_fig)

if __name__ == '__main__':
    app.run_server(debug=True)#, dev_tools_ui=False)

### Run with pytest don't ask why
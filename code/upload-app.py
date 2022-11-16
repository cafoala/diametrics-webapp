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
#import sys
#sys.path.append("/Users/cr591/OneDrive - University of Exeter/Desktop/diametrics/diametrics")
import preprocessing
import metrics_experiment
import periods

logging.basicConfig(level=logging.DEBUG)

external_stylesheets = [dbc.themes.JOURNAL]
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)



navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
        dbc.NavItem(dbc.NavLink("1 Trace Close Up", href="#")),
        dbc.NavItem(dbc.NavLink("Advanced Visualisations", href="#")),
        dbc.NavItem(dbc.NavLink("Periodic Analysis", href="#")),
        dbc.NavItem(dbc.NavLink("Theory & Code", href="#")),
        dbc.NavItem(dbc.NavLink("About Us", href="#")),
        ],
    brand="Diametrics",
    brand_href="#",
    color="dark",
    dark=True,
)
intro = html.Div(
    [
        html.H1('Diametrics'#, style={'textAlign': 'center'}
        ),
        html.P('A no-code webtool for calculating the metrics of glycemic control, creating visualisations and exploring CGM data',
                #style={'textAlign': 'center'}
                ),
    ]
)

upload_section= html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H2('Upload and process files'), width=7),
                dbc.Col(dcc.Upload(dbc.Button('Select Files', color="secondary"),
                    multiple=True,
                    id='upload-data',
               ))
            ]),
    
        html.Div(id='filelist', style={
                        'width': '80%',
                        'height': '100px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px',
                        'justify': "center",
                },),
    ],    
),

switches = html.Div(
    [
        dbc.Label("Toggle a bunch"),
        dbc.Checklist(
            options=[
                {"label": "Option 1", "value": 1},
                {"label": "Option 2", "value": 2},
                {"label": "Disabled Option", "value": 3, "disabled": True},
            ],
            value=[1],
            id="switches-input",
            switch=True,
        ),
    ]
)
metrics_section= html.Div(
    [
        html.H2('Calculate standard metrics '),
        dbc.Label('Metrics'), 
        dcc.Dropdown(['Lol', 'lolol']),
        switches,
        dbc.Button('Calculate metrics', id='calculate-metrics')
    ],    
    ),

content= html.Div([

        html.Div(
                id='output-data-upload',
                #style={
                #    'width': '80%',
                #    'height': '60px',
                #    'textAlign': 'center',
                #    'margin': '10px'
                #},
            ),
            html.Div(
                id='graph-section'
            ),
        ],
        ),
    
app.layout = html.Div([
    dbc.Col(navbar),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([dbc.Col(intro)
                ]),
            dbc.Button("Collapse options", color="primary", id="collapse-options", n_clicks=0),
            dbc.Row([
                dbc.Col(
                    dbc.Collapse(
                        dbc.Card(upload_section, body=True),
                        id="left-collapse",
                        is_open=True,
                    )
                ), 
                dbc.Col(
                    dbc.Collapse(
                        dbc.Card(metrics_section, body=True),
                        id="right-collapse",
                        is_open=True,
                    )
                ), 
            ]),
            dbc.Row([
                dbc.Col(content),

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

# Collapse left options panel once calculated
@app.callback(Output("left-collapse", "is_open"),
    Input("collapse-options", "n_clicks"), 
    Input('calculate-metrics', 'n_clicks'),
    State("left-collapse", "is_open"),
)
def toggle_left_options(n_toggle, n_metrics, is_open):
    if n_toggle or n_metrics:
        return not is_open
    return is_open

    
# Collapse options panel once calculated
@app.callback(Output("right-collapse", "is_open"),
    Input("collapse-options", "n_clicks"), 
    Input('calculate-metrics', 'n_clicks'),
    State("right-collapse", "is_open"),
)
def toggle_right_options(n_toggle, n_metrics, is_open):
    if n_toggle or n_metrics:
        return not is_open
    return is_open


# List the filenames
@app.callback(Output('filelist', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def list_files(list_of_contents, list_of_names):
    if list_of_contents is not None:
        return html.Div(
                    [i for i in list_of_names]
                )

# Create metrics table
@app.callback(Output('output-data-upload', 'children'),
              State('upload-data', 'contents'),
              Input('calculate-metrics', 'n_clicks'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))


def update_output(list_of_contents, n, list_of_names, list_of_dates):
    if n is not None:
        n = 0
        if list_of_contents is not None:

            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            
            
            data_details = pd.DataFrame.from_dict(children)[['Filename', 'ID', 'Usable', 'Device', 'Interval', 'Data Sufficiency', 'Start Time', 'End Time']]

            all_results = []
            day_results = []
            night_results = []

            for i in children:
                if i['Usable']==True:
                    df_id = i['data']
                    # Total df
                    all = metrics_experiment.calculate_all_metrics(df_id, ID=i['ID'], unit=i['Units'], interval=i['Interval'])
                    all_results.append(all)

                    # Breakdown df into night and day
                    df_day, df_night = periods.get_day_night_breakdown(df_id)
                    
                    # Daytime breakdown metrics 
                    day= metrics_experiment.calculate_all_metrics(df_day, ID=i['ID'], unit=i['Units'], interval=i['Interval'])
                    day_results.append(day)
                    
                    # Night breakdown metrics
                    night= metrics_experiment.calculate_all_metrics(df_night, ID=i['ID'], unit=i['Units'], interval=i['Interval'])
                    night_results.append(night)

            metrics = pd.DataFrame.from_dict(all_results).round(2) # this is stupid - already a dict
            print(metrics['AUC'])

            return html.Div([
                #html.H5(datetime.datetime.fromtimestamp(date)),
                
                html.Div([
                    html.H6('Data details'),

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
                    html.H6('Metrics of Glycemic Control'),
                    dash_table.DataTable(
                        id='metrics_tbl',
                        columns=[
                                    {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                                    if i == "iso_alpha3" or i == "Filename" or i == "id"
                                    else {"name": i, "id": i, "hideable": True, "selectable": True}
                                    for i in metrics.columns
                        ],
                        data=metrics.to_dict('records'),
                        style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    #'width':'200px'
                                },
                        
                        style_table={
                            'overflowX': 'auto',
                            #'height': 300,
                            },
                        #editable=True,              # allow editing of data inside all cells                        
                        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                        export_format="csv",
                        export_headers="display",
                        column_selectable='multi',
                        
                        ),
                    dcc.Store(id='metrics', data=metrics.to_dict('records')),
                    html.Hr()], #style={'display': 'block'}
                    ),
                    
                    dcc.Graph(
                        id='example-graph',
                        figure=px.bar(metrics, x='ID', y='Average glucose')
                )
            ], style={'display': 'block'})



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
    app.run_server(debug=True)

### Run with pytest don't ask why
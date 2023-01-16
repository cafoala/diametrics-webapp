#import base64
#import datetime
#import io
import os
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import logging
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
#import dash_uploader as du
#import preprocessing
#import metrics_experiment
#import periods
from dash.exceptions import PreventUpdate
import layout
#import layout_helper

# Import modules with section contents
import section_upload_content
import section_data_tbl
import section_analysis_options
import section_metrics_tbl
import section_overview_figs
import section_individual_figs
logging.basicConfig(level=logging.DEBUG)

external_stylesheets = [dbc.themes.JOURNAL]
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#, suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True

app.layout = layout.create_layout()

## COLLAPSIBLES ##
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
    Input('analysis-options-button', 'n_clicks'),
    State("data-tbl-collapse", "is_open"),
    prevent_initial_call=True)
def collapse_datatbl(n_toggle, n_metrics, is_open):
    if n_toggle or n_metrics:
        return not is_open# , not is_open]
    return is_open#, is_open]

# Collapse analysis options panel once calculated
@app.callback(Output('analysis-options-collapse', 'is_open'),
    Input("collapse-analysis-options-button", "n_clicks"), 
    Input('calculate-metrics', 'n_clicks'),
    State("analysis-options-collapse", "is_open"),
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

for section in [['metrics-tbl-collapse','metrics-button'], ['overview-figs-collapse','overview-figs-button'], ['individual-figs-collapse','individual-figs-button']]:
    @app.callback(Output(section[0], 'is_open'),
        Input(section[1], 'n_clicks'),
        State(section[0], 'is_open')
    )
    def toggle_buttons(n_clicks, is_open):
        if n_clicks:
            return not is_open# , not is_open]
        return is_open#, is_open]

## FILELIST ## 
# List the filenames
@app.callback(Output('filelist', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
    prevent_initial_call=True)
def list_files(list_of_contents, list_of_names):
    if list_of_contents is not None:

        file_list = section_upload_content.create_file_list(list_of_names)
        return file_list#, False

## DATA TABLE ##                
@app.callback([Output('raw-data-store', 'data'),
    Output('data-tbl', 'children')],
    Input('preprocess-button', 'n_clicks'),
    State('upload-data', 'last_modified'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True)
def preprocess_data(n_clicks, list_of_dates, list_of_contents, list_of_names):
    if n_clicks is None or list_of_dates is None:
        raise PreventUpdate
    children = [
        section_data_tbl.parse_contents(c, n, d) for c, n, d in
        zip(list_of_contents, list_of_names, list_of_dates)]
    
    data_table = section_data_tbl.create_data_table(children)
    
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

## ANALYSIS OPTIONS ##
# Layout
@app.callback(Output('analysis-options', 'children'),
        Input('analysis-options-button', 'n_clicks'),
        State('raw-data-store', 'data'),
        prevent_initial_call=True)
def select_options(n_clicks, raw_data):
    if n_clicks is None or raw_data is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate
   
    analysis_options_layout = section_analysis_options.get_analysis_options_layout()
    
    collapse_table = html.Div([
            dbc.Button('3. Analysis options', id='collapse-analysis-options-button'),                 
            dbc.Row([
                    dbc.Collapse(
                        dbc.Card(analysis_options_layout),
                        id="analysis-options-collapse",
                        is_open=True,
                    )
            ]),
        ])
    return collapse_table

def analysis_options_callbacks(app):
    @app.callback(Output('tir-sliders', 'children'),
            Input('add-tir-slider', 'n_clicks'),
            State('tir-sliders', 'children'),
            State('unit-type-options', 'value'))
    def create_range_slider(n_clicks, children, units):
        return section_analysis_options.create_range_slider(n_clicks, children, units)
    
    #@app.callback(Output())

analysis_options_callbacks(app)
# Update
'''@app.callback(
    Output('test-table', 'children'),
    #Input('unit-type', 'value'),
    Input('period-type', 'value'),
    State('metrics-store', 'data')
    )
def update_metrics_table(period, metrics_data):
    df = pd.DataFrame.from_dict(metrics_data)
    sub_df = df[df['period']==period].round(2)
    metrics_table = section_metrics_tbl.create_metrics_table(sub_df)
    #print(metrics_table.head())
    return metrics_table
'''

## METRICS TABLE ##
# Layout
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
    all_results = section_metrics_tbl.calculate_metrics(raw_data)
    #metrics = pd.DataFrame.from_dict(all_results).round(2) # this is stupid - already a dict
    
    metrics_layout = section_metrics_tbl.get_metrics_layout()
    
    collapse_table = html.Div([
            dbc.Button('3. Metrics', id='metrics-button'),                 
            dbc.Row([
                    dbc.Collapse(
                        dbc.Card(metrics_layout),
                        id="metrics-tbl-collapse",
                        is_open=True,
                    )
            ]),
        ])
    return all_results, collapse_table
# Update
@app.callback(
    Output('test-table', 'children'),
    #Input('unit-type', 'value'),
    Input('period-type', 'value'),
    State('metrics-store', 'data')
    )
def update_metrics_table(period, metrics_data):
    df = pd.DataFrame.from_dict(metrics_data)
    sub_df = df[df['period']==period].round(2)
    metrics_table = section_metrics_tbl.create_metrics_table(sub_df)
    #print(metrics_table.head())
    return metrics_table

## GROUP FIGS ##
# Layout
@app.callback(
    Output('group-figs', 'children'),
    #Input('calculate-metrics', 'n_clicks'),
    Input('metrics-store', 'modified_timestamp'),
    #State('metrics-store', 'data'),
    prevent_initial_call=True
)
def create_group_figs(ts):#, metrics):
    if ts is None:
        raise PreventUpdate
    options = ['Time in range', 'Average glucose', 'SD', 'CV', 'eA1c', 
    'Hypoglycemic episodes', 'AUC', 'MAGE', 'LBGI/HBGI']
    y_dropdown = dcc.Dropdown(options,
                'Time in range',
                id='yaxis-column'
        ),
    figs_layout = html.Div([
        dbc.Row([
                    dbc.Col(html.H2('Overview figures for participants')),
                    dbc.Col(y_dropdown),
        ]),
        dbc.Row([
                dbc.Col(id='bar-graph',),
                dbc.Col(id='box-plot',),

        ]),
        dbc.Row([
                dbc.Col(id='scatter-plot'),
                dbc.Col(id='summary-stats'),

        ])
    ])
    collapse_figs = html.Div([
            dbc.Button('4. Overview figures', id='overview-figs-button'),                 
            dbc.Row([
                    dbc.Collapse(
                        dbc.Card(figs_layout),
                        id="overview-figs-collapse",
                        is_open=True,
                    )
            ]),
        ])
    return collapse_figs
# Update
@app.callback(
    Output('bar-graph', 'children'),
    Output('box-plot', 'children'),
    #Output('scatter-plot', 'children'),
    #Output('summary-stats', 'children'),
    Input('yaxis-column', 'value'),
    Input('period-type', 'value'),
    State('metrics-store', 'data')
)
def update_group_figs(yaxis, period, data):
    df = pd.DataFrame.from_dict(data)
    sub_df = df[df['period']==period]
    bargraph = section_overview_figs.create_bargraph(sub_df, yaxis)
    boxplot = section_overview_figs.create_boxplot(sub_df, yaxis)
    #scatterplot, stats = section_overview_figs.create_scatter(sub_df, 'eA1c', 'TIR normal')
    return bargraph, boxplot, #scatterplot, stats

## INDIVIDUAL FIGS ##
@app.callback(
    Output('individual-figs', 'children'),
    #Input('calculate-metrics', 'n_clicks'),
    Input('metrics-store', 'modified_timestamp'),
    State('metrics-store', 'data'),
    prevent_initial_call=True
)
def create_individual_figs(ts, metrics):
    if ts is None:
        raise PreventUpdate
    df = pd.DataFrame.from_dict(metrics)
    subject_id = dcc.Dropdown(
                df['ID'].unique(),
                df['ID'].unique()[0],
                id='subject-id'
            ),
    figs_layout = html.Div([
        dbc.Row([
                    dbc.Col(html.H2('Closer look at individual participants')),
                    dbc.Col(subject_id),
        ]),
        dbc.Row([
                dbc.Col(id='amb-glc-profile',),
        ]),
        dbc.Row([
                dbc.Col(id='glc-trace'),
        ])
    ])
    collapse_figs = html.Div([
            dbc.Button('5. Individual breakdown', id='individual-figs-button'),                 
            dbc.Row([
                    dbc.Collapse(
                        dbc.Card(figs_layout),
                        id="individual-figs-collapse",
                        is_open=True,
                    )
            ]),
        ])
    return collapse_figs

@app.callback(
    Output('amb-glc-profile', 'children'),
    Output('glc-trace', 'children'),
    Input('subject-id', 'value'),
    State('raw-data-store', 'data'),
    #prevent_initial_call=True
)
def update_group_figs(subject_id, data):
    subject_data = next(item for item in data if item["ID"] == subject_id)
    df = pd.DataFrame.from_dict(subject_data['data'])
    agp = section_individual_figs.create_amb_glc_profile(df)
    glc_trace = section_individual_figs.create_glucose_trace(df)
    return agp, glc_trace


if __name__ == '__main__':
    # DASH_PORT is set to 80 in Dockerfile
    port = os.environ.get('DASH_PORT', 8050)
    app.run_server(debug=True,host='0.0.0.0',port=port)


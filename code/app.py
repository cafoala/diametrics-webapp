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
#import preprocessing
import metrics_experiment
import periods
from dash.exceptions import PreventUpdate
import layout
import layout_helper
# Import modules with content
import upload_content_section
import data_tbl_section
import metrics_tbl_section
import overview_figs_section
import individual_figs_section
#from preprocess_data_dash import *
logging.basicConfig(level=logging.DEBUG)

external_stylesheets = [dbc.themes.JOURNAL]
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#, suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True

app.layout = layout.create_layout()


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

for section in [['metrics-tbl-collapse','metrics-button'], ['overview-figs-collapse','overview-figs-button'], ['individual-figs-collapse','individual-figs-button']]:
    @app.callback(Output(section[0], 'is_open'),
        Input(section[1], 'n_clicks'),
        State(section[0], 'is_open')
    )
    def toggle_buttons(n_clicks, is_open):
        if n_clicks:
            return not is_open# , not is_open]
        return is_open#, is_open]

# List the filenames
@app.callback(Output('filelist', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
    prevent_initial_call=True)
def list_files(list_of_contents, list_of_names):
    if list_of_contents is not None:

        file_list = upload_content_section.create_file_list(list_of_names)
        return file_list#, False
                
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
        data_tbl_section.parse_contents(c, n, d) for c, n, d in
        zip(list_of_contents, list_of_names, list_of_dates)]
    
    data_table = data_tbl_section.create_data_table(children)
    
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
    all_results = metrics_tbl_section.calculate_metrics(raw_data)
    #metrics = pd.DataFrame.from_dict(all_results).round(2) # this is stupid - already a dict
    
    metrics_layout = metrics_tbl_section.get_metrics_layout()
    
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

@app.callback(
    Output('test-table', 'children'),
    #Input('unit-type', 'value'),
    Input('period-type', 'value'),
    State('metrics-store', 'data')
    )
def update_metrics_table(period, metrics_data):
    df = pd.DataFrame.from_dict(metrics_data)
    sub_df = df[df['period']==period].round(2)
    metrics_table = metrics_tbl_section.create_metrics_table(sub_df)
    #print(metrics_table.head())
    return metrics_table


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
    bargraph = overview_figs_section.create_bargraph(sub_df, yaxis)
    boxplot = overview_figs_section.create_boxplot(sub_df, yaxis)
    #scatterplot, stats = overview_figs_section.create_scatter(sub_df, 'eA1c', 'TIR normal')
    return bargraph, boxplot, #scatterplot, stats

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
            dbc.Button('4. Individual breakdown', id='individual-figs-button'),                 
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
    agp = individual_figs_section.create_amb_glc_profile(df)
    glc_trace = individual_figs_section.create_glucose_trace(df)
    return agp, glc_trace


if __name__ == '__main__':
    app.run_server(debug=True)#, dev_tools_ui=False)

### Run with pytest don't ask why
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table, ctx
import logging
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate
import layout
import warnings
warnings.filterwarnings('ignore')

# Import modules with section contents
import section_upload_content
import section_data_tbl
import section_analysis_options
import section_metrics_tbl
import section_overview_figs
import section_individual_figs
logging.basicConfig(level=logging.DEBUG)

external_stylesheets = [dbc.themes.BOOTSTRAP]
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#, suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True

app.layout = layout.create_tabs_layout()


@app.callback(Output('card-tabs', 'active_tab'),
    Input('preprocess-button', 'n_clicks'),
    Input('analysis-options-button', 'n_clicks'),
    Input('calculate-metrics', 'n_clicks'),
    prevent_initial_call=True)
def switch_tabs(n1, n2, n3):
    triggered_id = ctx.triggered_id
    print(triggered_id)
    if triggered_id=='preprocess-button':
        if n1 is None:
            raise PreventUpdate
        return 'data-tab'
    elif triggered_id == 'analysis-options-button':
        if n2 is None:
            raise PreventUpdate
        return 'other-metrics-tab'
    elif triggered_id == 'calculate-metrics':
        if n3 is None:
            raise PreventUpdate
        return 'metrics-tab'


for i in [['data-tab', 'preprocess-button'],['other-metrics-tab', 'analysis-options-button'], 
                ['metrics-tab', 'calculate-metrics'], ['indiv-vis', 'calculate-metrics'],
                ['external-tab', 'calculate-metrics']]:
    @app.callback(Output(i[0], 'disabled'),
                Input(i[1], 'n_clicks'),
                prevent_initial_call=True)
    def show_next_tab(n_clicks):
        if n_clicks is None:
            raise PreventUpdate
        return False


# CALLBACKS # 

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
    Output('data-tbl-div', 'children')],
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
    return (children, data_table)


## ANALYSIS OPTIONS ##
def analysis_options_callbacks(app):
    @app.callback(Output('tir-sliders', 'children'),
            Input('add-tir-slider', 'n_clicks'),
            State('tir-sliders', 'children'),
            State('unit-type-options', 'value'))
    def create_range_slider(n_clicks, children, units):
        return section_analysis_options.create_range_slider(n_clicks, children, units)
    
    #@app.callback(Output())

analysis_options_callbacks(app)


## METRICS TABLE ##
# Layout
@app.callback(Output('metrics-store', 'data'),
        #Output('metrics-tbl', 'children')],
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
    
    return all_results#, collapse_table
# Update
@app.callback(
    Output('test-table', 'children'),
    #Input('unit-type', 'value'),
    Input('metrics-store', 'data'),
    Input('period-type', 'value'),
    prevent_initial_call=True
    )
def update_metrics_table(metrics_data, period): 
    df = pd.DataFrame.from_dict(metrics_data)
    sub_df = df[df['period']==period].round(2)
    #sub_df = df
    metrics_table = section_metrics_tbl.create_metrics_table(sub_df)
    return metrics_table


## INDIVIDUAL FIGS ##
@app.callback(
    #Output('individual-figs', 'children'),
    #Input('calculate-metrics', 'n_clicks'),
    Output('subject-id-div', 'children'),
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
    return subject_id

@app.callback(
    Output('amb-glc-profile', 'children'),
    Output('glc-trace', 'children'),
    Output('pie-chart', 'children'),
    Input('subject-id', 'value'),
    State('raw-data-store', 'data'),
    #prevent_initial_call=True
)
def update_indiv_figs(subject_id, data):
    subject_data = next(item for item in data if item["ID"] == subject_id)
    df = pd.DataFrame.from_dict(subject_data['data'])
    agp = section_individual_figs.create_amb_glc_profile(df)
    glc_trace = section_individual_figs.create_glucose_trace(df)
    pie = section_individual_figs.create_pie_chart(df)
    return agp, glc_trace, pie



## GROUP FIGS ##
@app.callback(
    Output('bar-graph', 'children'),
    Output('box-plot', 'children'),
    #Output('scatter-plot', 'children'),
    #Output('summary-stats', 'children'),
    Input('yaxis-column', 'value'),
    Input('period-type', 'value'),
    State('metrics-store', 'data'),
    #prevent_initital_call=True
)
def update_group_figs(yaxis, period, data):
    if yaxis is None or period is None or data is None:
        raise PreventUpdate
    df = pd.DataFrame.from_dict(data)
    sub_df = df[df['period']==period]
    bargraph = section_overview_figs.create_bargraph(sub_df, yaxis)
    boxplot = section_overview_figs.create_boxplot(sub_df, yaxis)
    #scatterplot, stats = section_overview_figs.create_scatter(sub_df, 'eA1c', 'TIR normal')
    return bargraph, boxplot, #scatterplot, stats


if __name__ == '__main__':
    app.run_server(debug=True)#, dev_tools_ui=False)

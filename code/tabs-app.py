import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table, ctx
import logging
import os
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import layout
import warnings
warnings.filterwarnings('ignore')
import metrics_helper
# Import modules with section contents
import section_upload_content
import section_data_overview
import section_analysis_options
import section_metrics_tbl
import section_overview_figs
import section_individual_figs
import section_external_factors
import dash_uploader as du
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform
logging.basicConfig(level=logging.DEBUG)

external_stylesheets = [dbc.themes.BOOTSTRAP]
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
#app = DashProxy(transforms=[MultiplexerTransform()])
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#, suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True
#du.configure_upload(app, r"C:/tmp/Uploads")

app.layout = layout.create_tabs_layout()


@app.callback(Output('card-tabs', 'active_tab'),
    Input('preprocess-button', 'n_clicks'),
    Input('analysis-options-button', 'n_clicks'),
    Input('calculate-metrics', 'n_clicks'),
    prevent_initial_call=True)
def switch_tabs(n1, n2, n3):
    triggered_id = ctx.triggered_id
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
        section_data_overview.parse_contents(c, n, d) for c, n, d in
        zip(list_of_contents, list_of_names, list_of_dates)]
    data_table = section_data_overview.create_data_table(children)
    return (children, data_table)


@app.callback(
    Output('data-tbl', 'data'),
    Input('data-tbl', 'data_timestamp'),
    State('data-tbl', 'data'),
    State('raw-data-store', 'data'),
    #prevent_initial_call=True
    )
def update_columns(timestamp, rows, raw_data):
    for row in rows:
        # Calculate number of days
        try:
            row['Days'] = str(pd.to_datetime(row['End DateTime']) - pd.to_datetime(row['Start DateTime']))
        except:
            row['Days'] = 'NA'
        # Calculate data sufficiency
        #section_data_overview.calculate_data_sufficiency(row['Filename'], row['Start DateTime'], row['End DateTime'], raw_data)
        try:
            row['Data Sufficiency (%)'] = section_data_overview.calculate_data_sufficiency(row['Filename'], row['Start DateTime'], row['End DateTime'], raw_data)
        except: 
            row['Data Sufficiency (%)'] = 'NA'
    return rows

@app.callback(Output('processed-data-store', 'data'),
        Input('data-tbl', 'data_timestamp'),
        State('data-tbl', 'data'),
        State('raw-data-store', 'data'),
        )
def store_processed_data(time, table_data, raw_data):
    return section_data_overview.merge_glc_data(table_data, raw_data)

## ANALYSIS OPTIONS ##
def analysis_options_callbacks(app):
    @app.callback(Output('tir-sliders', 'children'),
            Input('add-tir-slider', 'n_clicks'),
            State('tir-sliders', 'children'),
            State('unit-type-options', 'value'),
            )
    def create_range_slider(n_clicks, children, units):
        if n_clicks is None:
            raise PreventUpdate
        return section_analysis_options.create_range_slider(n_clicks, children, units)
    
#all_sliders = ['tir_None', 'tir_1', 'tir_2', 'tir_3', 'tir_4', 'tir_5']   
all_sliders = ['tir-'+ str(i) for i in range(1, 50)]

for id in all_sliders:
    @app.callback(Output((id+'-heading'), 'children'),
        Input((id+'-slider'), 'drag_value'),
        )
    def print_heading(drag):
        drag_heading =f'Time in range {drag[0]}-{drag[1]} mmol/L'
        return drag_heading

    @app.callback(Output(id, 'children'),
            Input((id+'-button'), 'n_clicks'),
            )
    def remove_tir(n_clicks_remove):
        if n_clicks_remove is None:
            raise PreventUpdate
        return None


@app.callback(Output('tir-store', 'data'),
        Input('calculate-metrics', 'n_clicks'),
        State('tir-sliders', 'children')
        )
def update_store(clicks, children):
    if clicks is None:
        raise PreventUpdate
    if children is None:
        return None
    ranges = [i['props']['children']['props']['children'][1]['props']['children'][0]['props']['children'][0]['props']['children'][1]['props']['drag_value'] for i in children if i['props']['children']!=None]
    return ranges

analysis_options_callbacks(app)


## METRICS TABLE ##
# Layout
@app.callback(Output('asterix-day-time', 'children'),
        Input('start-day-time', 'value'),
        Input('end-day-time', 'value'),
        Input('start-night-time', 'value'),
        Input('end-night-time', 'value'),
)
def display_day_time(day_start, day_end, night_start, night_end):
    times = [i[11:16] for i in [day_start, day_end, night_start, night_end]]
    return html.P(f'* Day {times[0]}-{times[1]}, night {times[2]}-{times[3]}')

@app.callback(Output('metrics-store', 'data'),
        #Output('metrics-tbl', 'children')],
        Input('tir-store', 'data'),
        State('processed-data-store', 'data'),
        State('data-tbl','data'),
        State('lv1-hypo-slider', 'value'),
        State('lv2-hypo-slider', 'value'),
        State('lv1-hyper-slider', 'value'),
        State('lv2-hyper-slider', 'value'),
        State('calculate-metrics', 'n_clicks'),
        State('raw-data-store', 'data'),
        State('start-day-time', 'value'),
        State('end-day-time', 'value'),
        State('start-night-time', 'value'),
        State('end-night-time', 'value'),
        prevent_initial_call=True)
def calculate_metrics(additional_tirs, processed_data, edited_data, lv1_hypo, lv2_hypo, lv1_hyper, lv2_hyper, n_clicks, raw_data, day_start, day_end, night_start, night_end):
    if n_clicks is None or raw_data is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate
    times = [i[11:16] for i in [day_start, day_end, night_start, night_end]]
    #all_results = section_metrics_tbl.calculate_metrics(raw_data, edited_data, times[0], times[1], times[2], times[3], additional_tirs, lv1_hypo, lv2_hypo,  lv1_hyper, lv2_hyper)
        
    all_results = section_metrics_tbl.calculate_metrics(processed_data, times[0], times[1], times[2], times[3], additional_tirs, lv1_hypo, lv2_hypo,  lv1_hyper, lv2_hyper)

    #metrics = pd.DataFrame.from_dict(all_results).round(2) # this is stupid - already a dict
    
    return all_results#, collapse_table

# Update
@app.callback(
    Output('test-table', 'children'),
    Input('metrics-store', 'data'),
    Input('unit-type-options', 'value'),
    Input('period-type', 'value'),
    prevent_initial_call=True
    )
def update_metrics_table(metrics_data, units, period): 
    df = pd.DataFrame.from_dict(metrics_data)
    print(df.columns)
    if units == 'mmol/L':
        sub_df = np.round(df[(df['period']==period)&(df['units']==units)], 2)
        '''sub_df.columns = ['ID', 'Average glucose (mmol/L)', 'SD (mmol/L)', 
        'CV (mmol/L)', 'eA1c (%)', 'Min. glucose (mmol/L)',
       'Max. glucose (mmol/L)', 'AUC (mmol h/L)', 'LBGI', 'HBGI', 'MAGE (mmol/L)', 
       'TIR normal (%)', 'TIR hypoglycemia (%)', 'TIR level 1 hypoglycemia (%)',
       'TIR level 2 hypoglycemia (%)', 'TIR hyperglycemia (%)',
       'TIR level 1 hyperglycemia (%)', 'TIR level 2 hyperglycemia (%)', 
       'Total hypos (#)', 'LV1 hypos (#)', 'LV2 hypos (#)', 'Prolonged hypos (#)', 
       'Avg. length hypos','Total length hypos', 'Total hypers (#)', 
       'LV1 hypers (#)', 'LV2 hypers (#)',
       'Prolonged hypers (#)', 'Avg. length hypers', 'Total length hypers',
       'period', 'units']'''
    else:
        sub_df = np.round(df[(df['period']==period)&(df['units']==units)], 1)
        '''sub_df.columns = ['ID', 'Average glucose (mg/dL)', 'SD (mg/dL)', 
        'CV (mg/dL)', 'eA1c (%)', 'Min. glucose (mg/dL)',
       'Max. glucose (mg/dL)', 'AUC (mg h/dL)', 'LBGI', 'HBGI', 'MAGE (mg/dL)', 
       'TIR normal (%)', 'TIR hypoglycemia (%)', 'TIR level 1 hypoglycemia (%)',
       'TIR level 2 hypoglycemia (%)', 'TIR hyperglycemia (%)',
       'TIR level 1 hyperglycemia (%)', 'TIR level 2 hyperglycemia (%)', 
       'Total hypos (#)', 'LV1 hypos (#)', 'LV2 hypos (#)', 'Prolonged hypos (#)', 
       'Avg. length hypos','Total length hypos', 'Total hypers (#)', 
       'LV1 hypers (#)', 'LV2 hypers (#)', 'Prolonged hypers (#)', 
       'Avg. length hypers', 'Total length hypers',
       'period', 'units']'''
    sub_df = sub_df.drop(columns=['period', 'units'])
    metrics_table = section_metrics_tbl.create_metrics_table(sub_df, units)
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
    #State('raw-data-store', 'data'),
    State('processed-data-store', 'data'),
    #prevent_initial_call=True
)
def update_indiv_figs(subject_id, data):
    #subject_data = next(item for item in data if item["ID"] == subject_id)
    subject_data = pd.DataFrame(data)
    df = subject_data.loc[subject_data['ID']==subject_id]
    #df = pd.DataFrame.from_dict(subject_data['data'])
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

## ETERNAL FACTORS ##
@app.callback(
    Output("instructions-collapse", "is_open"),
    [Input("instructions-button", "n_clicks")],
    [State("instructions-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(Output('poi-datafile', 'children'),
    Output('poi-store', 'data'),
    Input('upload-poi-data', 'last_modified'),
    State('upload-poi-data', 'contents'),
    State('upload-poi-data', 'filename'),
    prevent_initial_call=True)
def poi(date, contents, filename):
    data = section_external_factors.parse_file(contents, filename, date)#.round(2)
    df = pd.DataFrame.from_dict(data)
    df['startDatetime'] = pd.to_datetime(df['startDatetime']).round('S').astype(str)
    df['endDatetime'] = pd.to_datetime(df['endDatetime']).round('S').astype(str)
    table = dash_table.DataTable(id='poi-data', data=df.to_dict('records'), 
            style_table={
                        'overflowX': 'auto',
                        'height': 300,
                        },)
    return table, data

@app.callback(Output('poi-metrics', 'children'),
    Input('periodic-metrics-button', 'n_clicks'),
    State('poi-store', 'data'),
    State('raw-data-store', 'data'),
    #State('processed-data-store', 'data'),
    prevent_initial_call=True)
def metrics(n_clicks, poi_data, raw_data):
    if n_clicks is None:
        raise PreventUpdate
    metrics = section_external_factors.calculate_periodic_metrics(poi_data, raw_data)
    table = section_external_factors.create_data_table(metrics)
    return table

if __name__ == '__main__':
    # DASH_PORT is set to 80 in Dockerfile
    port = os.environ.get('DASH_PORT', 8050)
    app.run_server(debug=True, host='0.0.0.0', port=port) #, dev_tools_ui=False)

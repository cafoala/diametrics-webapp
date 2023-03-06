import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table, ctx, callback
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
import datetime
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform
logging.basicConfig(level=logging.DEBUG)


app = dash.get_app()
# 1) configure the upload folder
du.configure_upload(app, r"C:\tmp\Uploads")

dash.register_page(__name__)
'''external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#, suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True

app.layout = layout.create_tabs_layout()'''
layout = layout.content #.create_tabs_layout()


@callback(Output('card-tabs', 'active_tab'),
    Input('data-overview-back-button', 'n_clicks'), # upload data
    Input('upload-next-button', 'n_clicks'), # data overview
    Input('analysis-options-back-button', 'n_clicks'), # data overview
    Input('data-overview-next-button', 'n_clicks'), # analysis options
    Input('standard-metrics-back-button', 'n_clicks'), # analysis options
    Input('analysis-options-next-button', 'n_clicks'), # standard metrics
    Input('indiv-vis-back-button', 'n_clicks'), # std metrics
    Input('standard-metrics-next-button', 'n_clicks'), # indiv vis
    Input('poi-back-button', 'n_clicks'), # indiv vis
    Input('indiv-vis-next-button', 'n_clicks'), # poi
    prevent_initial_call=True)
def switch_tabs(n1, n2, n3, n4, n5, n6, n7, n8, n9, n10):
    triggered_id = ctx.triggered_id
    if triggered_id=='data-overview-back-button':
        return 'upload-tab'
    if (triggered_id=='upload-next-button') or (triggered_id == 'analysis-options-back-button'):
        if n2 is None:
           raise PreventUpdate
        return 'data-tab'
    elif (triggered_id == 'data-overview-next-button') or (triggered_id == 'standard-metrics-back-button'):
        #if n2 is None:
         #   raise PreventUpdate
        return 'other-metrics-tab'
    elif (triggered_id == 'analysis-options-next-button') or (triggered_id == 'indiv-vis-back-button'):
        #if n3 is None:
         #   raise PreventUpdate
        return 'metrics-tab'
    elif (triggered_id == 'standard-metrics-next-button') or (triggered_id == 'poi-back-button'):
        #if n4 is None:
        #    raise PreventUpdate
        return 'indiv-vis'
    elif triggered_id == 'indiv-vis-next-button':
        #if n4 is None:
         #   raise PreventUpdate
        return 'external-tab'

# Disable button files uploaded
@callback(Output('upload-next-button', 'disabled'),
        Input('filelist', 'children'),
        prevent_initial_call=True)
def show_metrics_tab(children):
    return False

# Disable tab when button is clicked
@callback(Output('data-tab', 'disabled'),
        Input('upload-next-button', 'n_clicks'),
        prevent_initial_call=True)
def show_metrics_tab(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return False

# Undisable when data overview has loaded 
@callback(Output('other-metrics-tab', 'disabled'),
        Output('data-overview-next-button', 'disabled'),
        Input('data-tbl-div', 'children'),
        prevent_initial_call=True)
def show_metrics_tab(children):
    return False, False

# Undisable when metrics have loaded
@callback(Output('indiv-vis', 'disabled'),
        Output('external-tab', 'disabled'),
        Output('standard-metrics-next-button', 'disabled'),
        Input('test-table', 'children'),
        prevent_initial_call=True)
def show_metrics_tab(children):
    return False, False, False


for i in [#['data-tab', 'upload-next-button'],#['other-metrics-tab', 'data-overview-next-button'], 
                ['metrics-tab', 'analysis-options-next-button']]:#, ['indiv-vis', 'analysis-options-next-button'],
                #['external-tab', 'analysis-options-next-button']]:
    @callback(Output(i[0], 'disabled'),
                Input(i[1], 'n_clicks'),
                prevent_initial_call=True)
    def show_next_tab(n_clicks):
        if n_clicks is None:
            raise PreventUpdate
        return False


# CALLBACKS # 

## FILELIST ## 
# List the filenames
@callback(Output('filelist', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
    prevent_initial_call=True)
def list_files(list_of_contents, list_of_names):
    if list_of_contents is not None:

        file_list = section_upload_content.create_file_list(list_of_names)
        return file_list

'''@du.callback(
    output=Output('filelist', 'children'),
    id='dash-uploader',
)
def callback_on_completion(status: du.UploadStatus):
    filenames = [x.name for x in status.uploaded_files]
    file_list = section_upload_content.create_file_list(filenames)
    return file_list
    #return html.Ul([html.Li(str(x)) for x in status.uploaded_files])'''


## DATA TABLE ##                
'''@callback([Output('raw-data-store', 'data'),
    Output('data-tbl-div', 'children')],
    Input('upload-next-button', 'n_clicks'),
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
    return (children, data_table)'''

@callback([Output('raw-data-store', 'data'),
    Output('data-tbl-div', 'children')],
    Input('upload-next-button', 'n_clicks'),
    State('upload-data', 'last_modified'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('datetime-format', 'value'),
    prevent_initial_call=True)
def preprocess_data(n_clicks, list_of_dates, list_of_contents, list_of_names, dt_format):
    if n_clicks is None or list_of_dates is None:
        raise PreventUpdate
    children = [
        section_data_overview.read_files_2(c, n) for c, n in
                                                    zip(list_of_contents, list_of_names)]
    data_table = section_data_overview.create_data_table(children)
    return (children, data_table)

'''
@du.callback([Output('raw-data-store', 'data'),
    Output('data-tbl-div', 'children'),],
    id='dash-uploader')
def preprocess_data(status: du.UploadStatus):
    if not status.is_completed:
        raise PreventUpdate
    children = section_data_overview.read_files(status.uploaded_files)
    data_table = section_data_overview.create_data_table(children)
    return (children, data_table)

@du.callback([Output('raw-data-store', 'data'),
    Output('data-tbl-div', 'children')],
    id='dash-uploader')
def preprocess_data(status: du.UploadStatus):
    if not status.is_completed:
        raise PreventUpdate
    children = section_data_overview.read_files(status.uploaded_files)
    data_table = section_data_overview.create_data_table(children)
    return (children, data_table)
'''
@callback(
    Output('data-tbl', 'data'),
    Output('data-tbl', 'style_data_conditional'),
    Input('data-tbl', 'data_timestamp'),
    State('data-tbl', 'data'),
    State('raw-data-store', 'data'),
    #prevent_initial_call=True
    )
def update_columns(timestamp, rows, raw_data):
    for row in rows:
        # Calculate number of days
        try:
            days = pd.to_datetime(row['End DateTime']) - pd.to_datetime(row['Start DateTime'])
            if days <= datetime.timedelta(minutes=1):
                days ='N/A'
        except:
            days = 'N/A'
        row['Days'] = str(days)
        
        # Calculate data sufficiency
        if days != 'N/A':
            try:
                data_suff = section_data_overview.calculate_data_sufficiency(row['Filename'], 
                                                                        row['Start DateTime'], 
                                                                        row['End DateTime'], 
                                                                        raw_data)
            except: 
                data_suff = 'N/A'
        else:
            data_suff = 'N/A'
        row['Data Sufficiency (%)'] = data_suff
    style_conds = section_data_overview.create_conditional_formatting(rows)
    return rows, style_conds

@callback(Output('processed-data-store', 'data'),
        Input('data-tbl', 'data_timestamp'),
        State('data-tbl', 'data'),
        State('raw-data-store', 'data'),
        )
def store_processed_data(time, table_data, raw_data):
    return section_data_overview.merge_glc_data(table_data, raw_data)

## ANALYSIS OPTIONS ##
#def analysis_options_callbacks(app):
@callback(Output('tir-sliders', 'children'),
        Input('add-tir-slider', 'n_clicks'),
        State('tir-sliders', 'children'),
        State('unit-type-options', 'value'),
        prevent_initial_call=True
        )
def create_range_slider(n_clicks, children, units):
    if n_clicks is None:
        raise PreventUpdate
    return section_analysis_options.create_range_slider(n_clicks, children, units)

#analysis_options_callbacks(app)

all_sliders = ['tir-'+ str(i) for i in range(1, 10)]

for id in all_sliders:
    @callback(Output((id+'-heading'), 'children'),
        Input((id+'-slider'), 'drag_value'),
        prevent_initial_call=True
        )
    def print_heading(drag):
        drag_heading =f'Time in range {drag[0]}-{drag[1]} mmol/L'
        return drag_heading

    @callback(Output(id, 'children'),
            Input((id+'-button'), 'n_clicks'),
            prevent_initial_call=True
            )
    def remove_tir(n_clicks_remove):
        if n_clicks_remove is None:
            raise PreventUpdate
        return None


@callback(Output('tir-store', 'data'),
        Input('analysis-options-next-button', 'n_clicks'),
        State('tir-sliders', 'children'),
        prevent_initial_call=True
        )
def update_store(clicks, children):
    if clicks is None:
        raise PreventUpdate
    if children is None:
        return None
    ranges = [i['props']['children']['props']['children'][1]['props']['children'][0]['props']['children'][0]['props']['children'][1]['props']['drag_value'] for i in children if i['props']['children']!=None]
    return ranges


## METRICS TABLE ##
# Layout
@callback(Output('asterix-day-time', 'children'),
        Input('start-day-time', 'value'),
        Input('end-day-time', 'value'),
        Input('start-night-time', 'value'),
        Input('end-night-time', 'value'),
)
def display_day_time(day_start, day_end, night_start, night_end):
    times = [i[11:16] for i in [day_start, day_end, night_start, night_end]]
    return html.P(f'* Day {times[0]}-{times[1]}, night {times[2]}-{times[3]}')

@callback(Output('metrics-store', 'data'),
        #Output('metrics-tbl', 'children')],
        Input('tir-store', 'data'),
        State('processed-data-store', 'data'),
        State('data-tbl','data'),
        State('lv1-hypo-slider', 'value'),
        State('lv2-hypo-slider', 'value'),
        State('lv1-hyper-slider', 'value'),
        State('lv2-hyper-slider', 'value'),
        State('short-events-mins', 'value'),
        State('prolonged-events-mins', 'value'),
        State('analysis-options-next-button', 'n_clicks'),
        State('raw-data-store', 'data'),
        State('start-day-time', 'value'),
        State('end-day-time', 'value'),
        State('start-night-time', 'value'),
        State('end-night-time', 'value'),
        prevent_initial_call=True)
def calculate_metrics(additional_tirs, processed_data, edited_data, lv1_hypo, lv2_hypo, lv1_hyper, lv2_hyper, short_mins, long_mins, n_clicks, raw_data, day_start, day_end, night_start, night_end):
    if n_clicks is None or raw_data is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate
    times = [i[11:16] for i in [day_start, day_end, night_start, night_end]]
    #all_results = section_metrics_tbl.calculate_metrics(raw_data, edited_data, times[0], times[1], times[2], times[3], additional_tirs, lv1_hypo, lv2_hypo,  lv1_hyper, lv2_hyper)
        
    all_results = section_metrics_tbl.calculate_metrics(processed_data, times[0], times[1], times[2], times[3], additional_tirs, lv1_hypo, lv2_hypo,  lv1_hyper, lv2_hyper, short_mins, long_mins, )

    #metrics = pd.DataFrame.from_dict(all_results).round(2) # this is stupid - already a dict
    
    return all_results#, collapse_table

# Update
@callback(
    Output('test-table', 'children'),
    Input('metrics-store', 'data'),
    Input('unit-type-options', 'value'),
    Input('period-type', 'value'),
    prevent_initial_call=True
    )
def update_metrics_table(metrics_data, units, period): 
    df = pd.DataFrame.from_dict(metrics_data)
    if units == 'mmol/L':
        sub_df = np.round(df[(df['period']==period)&(df['units']==units)], 2)
    else:
        sub_df = np.round(df[(df['period']==period)&(df['units']==units)], 1)
    sub_df = section_metrics_tbl.change_headings(sub_df, units)
    sub_df = sub_df.drop(columns=['period', 'units'])
    metrics_table = section_metrics_tbl.create_metrics_table(sub_df)
    return metrics_table


## INDIVIDUAL FIGS ##
@callback(
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

@callback(
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
@callback(
    Output('bar-graph', 'children'),
    Output('box-plot', 'children'),
    #Output('scatter-plot', 'children'),
    #Output('summary-stats', 'children'),
    Input('yaxis-column', 'value'),
    Input('period-type', 'value'),
    Input('unit-type-options', 'value'),
    State('metrics-store', 'data'),
    #prevent_initital_call=True
)
def update_group_figs(yaxis, period, units, data):
    if yaxis is None or period is None or data is None:
        raise PreventUpdate
    df = pd.DataFrame.from_dict(data)
    sub_df = df[(df['period']==period)&(df['units']==units)]
    bargraph = section_overview_figs.create_bargraph(sub_df, yaxis)
    boxplot = section_overview_figs.create_boxplot(sub_df, yaxis)
    #scatterplot, stats = section_overview_figs.create_scatter(sub_df, 'eA1c', 'TIR normal')
    return bargraph, boxplot, #scatterplot, stats

## ETERNAL FACTORS ##
@callback(
    Output("instructions-collapse", "is_open"),
    [Input("instructions-button", "n_clicks")],
    [State("instructions-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(Output('poi-sliders', 'children'),
            Input('add-poi-slider', 'n_clicks'),
            State('poi-sliders', 'children')
            )
def create_range_slider(n_clicks, children):
    return section_external_factors.create_range_slider(n_clicks, children)
    
all_sliders_poi = ['poi-None']+['poi-'+ str(i) for i in range(1, 10)]

for id in all_sliders_poi:
    @callback(Output((id+'-heading'), 'children'),
        Input((id+'-slider'), 'drag_value'),
        )
    def print_heading(drag):
        first, last, first_num, last_num = section_external_factors.drag_values(drag)
        drag_heading =f'{first} to {last}'
        return drag_heading

    @callback(Output(id, 'children'),
            Input((id+'-button'), 'n_clicks'),
            )
    def remove_poi(n_clicks_remove):
        if n_clicks_remove is None:
            raise PreventUpdate
        return None


@callback(Output('ranges-store', 'data'),
          Output('poi-collapse-3', 'is_open'),
            Input('periodic-metrics-button', 'n_clicks'),
            State('poi-sliders', 'children')
        )
def update_store(clicks, children):
    if clicks is None:
        raise PreventUpdate
    if children is None:
        raise PreventUpdate
    ranges = [i['props']['children']['props']['children'][0]['props']['children'][1]['props']['children'][0]['props']['children'][0]['props']['drag_value'] for i in children if i['props']['children']!=None]
    return ranges, True

@callback(Output('poi-datafile', 'children'),
    Output('poi-store', 'data'),
    Input('upload-poi-data', 'last_modified'),
    State('upload-poi-data', 'contents'),
    State('upload-poi-data', 'filename'),
    prevent_initial_call=True)
def poi(date, contents, filename):
    data = section_external_factors.parse_file(contents, filename, date)#.round(2)
    if data=='columns':
        table = dbc.Alert(
            "Your file doesn't have the correct headings!",
            id="alert-columns",
            dismissable=True,
            is_open=True,
            color='danger'
        )
        return table, None

    elif data=='format':
        table = dbc.Alert(
            "Your file isn't in the correct format - csv, excel or txt only!",
            id="alert-format",
            dismissable=True,
            is_open=True,
            color='danger'
        )
        return table, None
    else:
        df = pd.DataFrame.from_dict(data)
        df['Start of event'] = pd.to_datetime(df['Start of event']).round('S').astype(str)
        df['End of event'] = pd.to_datetime(df['End of event']).round('S').astype(str)
        df['ID'] = df['ID'].astype(str)
        table = dash_table.DataTable(id='poi-data', data=df.to_dict('records'), 
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
                                                'maxHeight': '20vh',
                                                },
                                            
                                            style_header={
                                                'backgroundColor': 'rgb(210, 210, 210)',
                                                'color': 'black',
                                                #'fontWeight': 'bold'
                                            },)
        return table, data

@callback(#Output('poi-metrics', 'children'),
    Output('poi-metrics-store', 'data'),
    Input('ranges-store', 'data'),
    State('set-periods-poi-checklist', 'value'),
    State('poi-store', 'data'),
    State('raw-data-store', 'data'),
    State('tir-store', 'data'),
    State('lv1-hypo-slider', 'value'),
    State('lv2-hypo-slider', 'value'),
    State('lv1-hyper-slider', 'value'),
    State('lv2-hyper-slider', 'value'),
    State('short-events-mins', 'value'),
    State('prolonged-events-mins', 'value'),
    #State('start-day-time', 'value'),
    #State('end-day-time', 'value'),
    State('start-night-time', 'value'),
    State('end-night-time', 'value'),
    prevent_initial_call=True)
def metrics(poi_ranges, set_periods, poi_data, raw_data, additional_tirs, lv1_hypo, lv2_hypo, lv1_hyper, lv2_hyper, short_mins, long_mins, night_start, night_end): # day_start, day_end, night_start, night_end
    if poi_ranges is None:
        raise PreventUpdate
    if poi_data is None:
        return dbc.Alert(
            "Oops! You haven't uploaded your periods file. Go back to step 1 to upload your data",
            id="alert-fade",
            dismissable=True,
            is_open=True,
            color='danger'
        ),
    if raw_data is None:
        return dbc.Alert(
            "You haven't uploaded any CGM data! Go back to page 1 to upload your CGM data",
            id="alert-fade",
            dismissable=True,
            is_open=True,
            color='danger'
        ),
    #print(set_periods)
    metrics = section_external_factors.calculate_periodic_metrics(poi_ranges, set_periods, poi_data, raw_data, additional_tirs, lv1_hypo, lv2_hypo, lv1_hyper, lv2_hyper, short_mins, long_mins, night_start, night_end) #, day_start, day_end, night_start, night_end
    #print(metrics)
    return metrics


# Update
@callback(
    Output('poi-metrics', 'children'),
    Input('poi-metrics-store', 'data'),
    Input('poi-unit-options', 'value'),
    prevent_initial_call=True
    )
def update_poi_metrics_table(metrics_data, units): 
    df = pd.DataFrame.from_dict(metrics_data)
    if units == 'mmol/L':
        sub_df = np.round(df[df['units']==units], 2)
        
    else:
        sub_df = np.round(df[df['units']==units], 1)

    sub_df = section_metrics_tbl.change_headings(sub_df, units)
    sub_df = sub_df.drop(columns=['units']) #'period', 
    table = section_external_factors.create_data_table(sub_df)
    return table

@callback(Output('poi-2-collapse', 'is_open'),
          Input('poi-data', 'data'),
          )
def open_collapse(data):
    return True

'''if __name__ == '__main__':
    # DASH_PORT is set to 80 in Dockerfile
    port = os.environ.get('DASH_PORT', 8050)
    app.run_server(debug=True, host='0.0.0.0', port=port) #, dev_tools_ui=False)'''

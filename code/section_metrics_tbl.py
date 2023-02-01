from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import metrics_experiment
import periods
from pandarallel import pandarallel
pandarallel.initialize()

def get_metrics_layout():
    units = dbc.RadioItems(
                id="unit-type-options",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": 'mmol/L', "value": 'mmol/L'},
                    {"label": "mg/dL", "value": 'mg/dL'},
                    #{"label": "Both", "value": 'both'},
                ],
                value='mmol/L',
                style={'textAlign': 'center'}
            ),

    time_period = dbc.RadioItems(
            id="period-type",
            class_name="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "All", "value": 'All'},
                {"label": "Day", "value": 'Day'},
                {"label": "Night", "value": 'Night'},
            ],
            value='All',
        ),

    
    options = ['Time in range', 'Average glucose', 'SD', 'CV', 'eA1c', 
    'Hypoglycemic episodes', 'AUC', 'MAGE', 'LBGI/HBGI']
    
    metrics_layout = html.Div([
        html.H2('Metrics of Glycemic Control'),
        dbc.Row([
                dbc.Col(width=5),
                dbc.Col(units, width=3),
                dbc.Col(time_period, width=3),
        ]),

        html.Div(id='asterix-day-time', style={'textAlign': 'right'}),
        dbc.Row([
                dbc.Col(dbc.Spinner(spinner_style={"width": "3rem", "height": "3rem"}), id='test-table'),
        ]),
    ])
    return metrics_layout
    
'''def calculate_metrics(raw_data, edited_data, day_start, day_end, night_start, night_end, additional_tirs, lv1_hypo, lv2_hypo, lv1_hyper, lv2_hyper): #
    all_results = []
    #edited_data = pd.DataFrame(edited_data)
    for i in raw_data:
        if i['Usable']==True:
            edited_row = [j for j in edited_data if j['Filename']==i['Filename']][0]
            ID = edited_row['ID']#.values[0]
            start = edited_row['Start DateTime']#.values[0]
            end = edited_row['End DateTime']#.values[0]
            df_id = pd.DataFrame.from_dict(i['data'])
            df_id.time = pd.to_datetime(df_id.time)
            df_id = df_id[(df_id['time']>=start)&(df_id['time']<=end)]
            # Total df
            all, all_mg = metrics_experiment.calculate_all_metrics(df_id, ID=ID, 
                                units=i['Units'], 
                                additional_tirs=additional_tirs, lv1_hypo=lv1_hypo, 
                                lv2_hypo=lv2_hypo, lv1_hyper=lv1_hyper, 
                                lv2_hyper=lv2_hyper)
            # mmol
            all['period'] = 'All'
            all['units'] = 'mmol/L'
            all_results.append(all)
            # mg
            all_mg['period'] = 'All'
            all_mg['units'] = 'mg/dL'
            all_results.append(all_mg)

            # Breakdown df into night and day
            df_day, df_night = periods.get_day_night_breakdown(df_id, day_start, day_end, night_start, night_end)
            
            # Daytime breakdown metrics 
            day, day_mg= metrics_experiment.calculate_all_metrics(df_day, ID=ID, 
                                units=i['Units'], 
                                additional_tirs=additional_tirs, lv1_hypo=lv1_hypo, 
                                lv2_hypo=lv2_hypo, lv1_hyper=lv1_hyper, 
                                lv2_hyper=lv2_hyper)
            # mmol
            day['period'] = 'Day'
            day['units'] = 'mmol/L'
            all_results.append(day)
            # mg
            day_mg['period'] = 'Day'
            day_mg['units'] = 'mg/dL'
            all_results.append(day_mg)
            
            # Night breakdown metrics
            night, night_mg= metrics_experiment.calculate_all_metrics(df_night, ID=ID, 
                                units=i['Units'], 
                                additional_tirs=additional_tirs, lv1_hypo=lv1_hypo, 
                                lv2_hypo=lv2_hypo, lv1_hyper=lv1_hyper, 
                                lv2_hyper=lv2_hyper)
            # mmol
            night['period'] = 'Night'
            night['units'] = 'mmol/L'
            all_results.append(night)
            # mg
            night_mg['period'] = 'Night'
            night_mg['units'] = 'mg/dL'
            all_results.append(night_mg)

    return all_results'''

def get_metrics_breakdown(df_id, day_start, day_end, night_start, night_end, 
                        additional_tirs, lv1_hypo, 
                        lv2_hypo, lv1_hyper, 
                        lv2_hyper):
    all_results = pd.DataFrame()
    df_id['time'] = pd.to_datetime(df_id['time'])
    # Total df
    all, all_mg = metrics_experiment.calculate_all_metrics(df_id, 
                        #ID='blob', units=i['Units'], 
                        additional_tirs=additional_tirs, lv1_hypo=lv1_hypo, 
                        lv2_hypo=lv2_hypo, lv1_hyper=lv1_hyper, 
                        lv2_hyper=lv2_hyper)
    # mmol
    all['period'] = 'All'
    all['units'] = 'mmol/L'
    all_results = all_results.append(all)

    # mg
    all_mg['period'] = 'All'
    all_mg['units'] = 'mg/dL'
    all_results = all_results.append(all_mg)

    df_day, df_night = periods.get_day_night_breakdown(df_id, day_start, day_end, night_start, night_end)
    
    # Daytime breakdown metrics 
    day, day_mg = metrics_experiment.calculate_all_metrics(df_day, 
                        #ID=ID, units=i['Units'], 
                        additional_tirs=additional_tirs, lv1_hypo=lv1_hypo, 
                        lv2_hypo=lv2_hypo, lv1_hyper=lv1_hyper, 
                        lv2_hyper=lv2_hyper)
    
    # mmol
    day['period'] = 'Day'
    day['units'] = 'mmol/L'
    all_results = all_results.append(day)

    # mg
    day_mg['period'] = 'Day'
    day_mg['units'] = 'mg/dL'
    all_results = all_results.append(day_mg)
    
    # Night breakdown metrics
    night, night_mg= metrics_experiment.calculate_all_metrics(df_night,
                        #ID=ID, units=i['Units'], 
                        additional_tirs=additional_tirs, lv1_hypo=lv1_hypo, 
                        lv2_hypo=lv2_hypo, lv1_hyper=lv1_hyper, 
                        lv2_hyper=lv2_hyper)
    
    # mmol
    night['period'] = 'Night'
    night['units'] = 'mmol/L'
    all_results = all_results.append(night)
    
    # mg
    night_mg['period'] = 'Night'
    night_mg['units'] = 'mg/dL'
    all_results = all_results.append(night_mg)
    return all_results


def calculate_metrics(processed_data, day_start, day_end, night_start, night_end, additional_tirs, lv1_hypo, lv2_hypo, lv1_hyper, lv2_hyper): #
    # Breakdown df into night and day
    processed_data = pd.DataFrame(processed_data)
    all_results = processed_data.groupby('ID').parallel_apply(lambda group: 
                                get_metrics_breakdown(group, day_start, 
                                day_end, night_start, night_end, additional_tirs, 
                                lv1_hypo, lv2_hypo, lv1_hyper, lv2_hyper))
    all_results = all_results.reset_index().drop(columns='level_1')
    all_results = all_results.to_dict('records')
    return all_results
        
def create_metrics_table(df):
    options = ['Time in range', 'Average glucose', 'SD', 'CV', 'eA1c', 
        'Hypoglycemic episodes', 'AUC', 'MAGE', 'LBGI', 'HBGI']    
    
    data_table= dash_table.DataTable(
                #id='metrics_tbl',
                columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                            if i == "iso_alpha3" or i == "ID" or i == "id"
                            else {"name": i, "id": i, "hideable": True, "selectable": True}
                            for i in df.columns
                ],
                data=df.to_dict('records'),
                style_cell={
                            'whiteSpace': 'normal',
                },
                style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'width':'200px'
                        },
                
                style_table={
                    'overflowX': 'auto',
                    'height': 300,
                    },
                #editable=True,              # allow editing of data inside all cells                        
                filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                fixed_rows={'headers':True},
                #fixed_columns={'headers': True, 'data': 1},
                export_format="csv",
                export_headers="display",
                column_selectable='multi',
                fill_width=False,
                tooltip_header={
                        'LBGI':'Low blood glucose index',
                        'HBGI': 'High blood glucose index'

                    },
                )
    return html.Div([
            dbc.Row(data_table),
            dbc.Row([
                dbc.Col(html.H4('Overview figures')),
                dbc.Col(dcc.Dropdown(options,
                    'Time in range',
                    id='yaxis-column')
                ),
            ]),
            dbc.Row([
                dbc.Col(id='bar-graph'),
                dbc.Col(id='box-plot')
            ])
        ])
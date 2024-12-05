from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import metrics_experiment
import metrics_helper
import periods


def get_metrics_layout():
    units = html.Div(dbc.RadioItems(
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
            ), className="radio-group"
        )

    time_period = html.Div(dbc.RadioItems(
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
        ), className="radio-group"
                        )
    

    
    '''options = ['Time in range', 'Average glucose', 'SD', 'CV', 'eA1c', 
    'Glycemic episodes', 'AUC', 'MAGE', 'LBGI/HBGI']'''
    
    metrics_layout = html.Div([
        dbc.Row([
            dbc.Col(
                html.H2('Metrics of Glycemic Control')),
            dbc.Col(
                html.Div(id='asterix-day-time', style={'textAlign': 'right'})
            )
        ]),
        dbc.Row([
                dbc.Col(width=4),
                dbc.Col([dbc.Button('Download Raw CGM Data', id='download-combined-button', color='primary'),  
                        dcc.Download(id="download-dataframe-csv")],width=2,),
                dbc.Col(units, width=3, style={'textAlign': 'right'}),
                dbc.Col(time_period, width=3, style={'textAlign': 'right'}),
        ]),
        html.Div([
            html.Br(),
            html.Br(),
            dbc.Spinner(spinner_style={"width": "3rem", "height": "3rem"})
                  ], 
        id='test-table', style={'textAlign': 'center'})
    ])
    return metrics_layout


def get_metrics_breakdown(df_id, day_start, day_end, night_start, night_end, 
                        additional_tirs, lv1_hypo, lv2_hypo, lv1_hyper, 
                        lv2_hyper, short_mins, long_mins):
    all_results = pd.DataFrame()
    df_id['time'] = pd.to_datetime(df_id['time'])

    #info = metrics_helper.helper_missing(df_id, interval, None, None)
    #info = pd.DataFrame.from_dict(info, orient='index').T
    info = pd.DataFrame()
    # Total df
    all, all_mg = metrics_experiment.calculate_all_metrics(df_id, 
                        #ID='blob', units=i['Units'], 
                        additional_tirs=additional_tirs,
                        lv1_hypo=lv1_hypo, 
                        lv2_hypo=lv2_hypo, 
                        lv1_hyper=lv1_hyper, 
                        lv2_hyper=lv2_hyper, 
                        event_mins=short_mins, 
                        event_long_mins=long_mins)
    
    # mmol
    all['period'] = 'All'
    all['units'] = 'mmol/L'
    #all = {**info, **all}
    all = pd.concat([info, all],axis=1)

    all_results = all_results.append(all)

    # mg
    all_mg['period'] = 'All'
    all_mg['units'] = 'mg/dL'
    all_mg = pd.concat([info, all_mg],axis=1)
    all_results = all_results.append(all_mg)

    df_day, df_night = periods.get_day_night_breakdown(df_id, day_start, day_end, night_start, night_end)
    if not df_day.empty:
        # Daytime breakdown metrics 
        day, day_mg = metrics_experiment.calculate_all_metrics(df_day, 
                            #ID=ID, units=i['Units'], 
                            additional_tirs=additional_tirs, lv1_hypo=lv1_hypo, 
                            lv2_hypo=lv2_hypo, lv1_hyper=lv1_hyper, 
                            lv2_hyper=lv2_hyper, event_mins=short_mins, 
                            event_long_mins=long_mins)
        # mmol
        day['period'] = 'Day'
        day['units'] = 'mmol/L'
        day = pd.concat([info, day],axis=1)

        
        # mg
        day_mg['period'] = 'Day'
        day_mg['units'] = 'mg/dL'
        day_mg = pd.concat([info, day_mg],axis=1)

        
    else:
        day = pd.DataFrame({'period':['Day'], 'units':['mmol/L']})
        day = pd.concat([info, day],axis=1)
        
        day_mg = pd.DataFrame({'period':['Day'], 'units':['mg/dL']})
        day_mg = pd.concat([info, day_mg],axis=1)
    if not df_night.empty:

        # Night breakdown metrics
        night, night_mg= metrics_experiment.calculate_all_metrics(df_night,
                            #ID=ID, units=i['Units'], 
                            additional_tirs=additional_tirs, lv1_hypo=lv1_hypo, 
                            lv2_hypo=lv2_hypo, lv1_hyper=lv1_hyper,
                            lv2_hyper=lv2_hyper, event_mins=short_mins,
                            event_long_mins=long_mins)
        # mmol  
        night['period'] = 'Night'
        night['units'] = 'mmol/L'  
        night = pd.concat([info, night],axis=1)
        # mg
        night_mg['period'] = 'Night'
        night_mg['units'] = 'mg/dL'
        night_mg = pd.concat([info, night_mg],axis=1)
    else:
        night = pd.DataFrame({'period':['Night'], 'units':['mmol/L']})
        night = pd.concat([info, night],axis=1)
        night_mg = pd.DataFrame({'period':['Night'], 'units':['mg/dL']})
        night_mg = pd.concat([info, night_mg],axis=1)
    
    all_results = all_results.append(day)
    all_results = all_results.append(day_mg)
    all_results = all_results.append(night)
    all_results = all_results.append(night_mg)
    return all_results

 

def calculate_metrics(processed_data, day_start, day_end, night_start, 
                            night_end, additional_tirs, lv1_hypo, lv2_hypo,
                            lv1_hyper, lv2_hyper, short_mins, long_mins): #
    # Breakdown df into night and day
    processed_data = pd.DataFrame(processed_data)

    all_results = processed_data.groupby('ID').apply(lambda group: 
                                get_metrics_breakdown(group, day_start, 
                                day_end, night_start, night_end, additional_tirs, 
                                lv1_hypo, lv2_hypo, lv1_hyper, lv2_hyper, short_mins, long_mins))
    all_results = all_results.reset_index().drop(columns='level_1')
    all_results = all_results.to_dict('records')
    return all_results

def change_headings(df, units):
    if units == 'mmol/L':
        return df.rename(columns={'Average glucose':'Average glucose (mmol/L)','SD':'SD (mmol/L)', 
                    'Min. glucose':'Min.glucose (mmol/L)',
                    'Max. glucose':'Max. glucose (mmol/L)', 'AUC':'AUC (mmol h/L)', 
                    'MAGE':'MAGE (mmol/L)', 'TIR normal':'Time in range 3.9-10mmol/L (%)',
                    'TIR normal 1':'Time in range 3.9-7.8mmol/L (%)',
                    'TIR normal 2':'Time in range 7.8-10mmol/L (%)',
                    'TIR level 1 hypoglycemia':'Time in range 3.0-3.9 mmol/L (%)', 
                    'TIR level 2 hypoglycemia':'Time in range <3.0 mmol/L (%)',
                    'TIR level 1 hyperglycemia':'Time in range 10-13.9 mmol/L (%)', 
                    'TIR level 2 hyperglycemia':'Time in range >13.9 mmol/L (%)',})
    else:
        return df.rename(columns={'Average glucose':'Average glucose (mg/dL)','SD':'SD (mg/dL)', 
                    'Min. glucose':'Min. glucose (mg/dL)',
                    'Max. glucose':'Max. glucose (mg/dL)', 'AUC':'AUC (mg h/dL)', 
                    'MAGE':'MAGE (mg/dL)', 'TIR normal':'Time in range 70-180mg/dL (%)',
                    'TIR normal 1':'Time in range 70-140mg/dL (%)',
                    'TIR normal 2':'Time in range 140-180mg/dL (%)',
                    'TIR level 1 hypoglycemia':'Time in range 70–54mg/dL (%)', 
                    'TIR level 2 hypoglycemia':'Time in range <54mg/dL (%)',
                    'TIR level 1 hyperglycemia':'Time in range 180-250mg/dL (%)', 
                    'TIR level 2 hyperglycemia':'Time in range >250mg/dL (%)',})

def create_metrics_table(df):
    df = df.fillna('N/A')
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
                        'font-family':'sans-serif',
                        'textAlign':'center',
                        'backgroundColor':'white'
                },

                style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'width':'200px'
                        },
                
                style_table={
                    'overflowX': 'auto',
                    'maxHeight': 300,
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
        
    options = ['Time in range', 'Average glucose', 'SD', 'CV', 'eA1c', 
        'Total glycemic events', 'Hypoglycemic events',
        'Hyperglycemic events', 'Prolonged glycemic events', 
        'AUC', 'MAGE', 'LBGI', 'HBGI']   
    return html.Div([
            dbc.Row(data_table),
            html.Br(),
            html.Hr(),
            html.H3('Overview figures'),
            dbc.Row([
                dbc.Col(),
                dbc.Col(dcc.Dropdown(options,
                    'Time in range',
                    id='yaxis-column'), width=3
                ),
            ]),
            dbc.Row([
                dbc.Col(id='bar-graph')
            ]),
            dbc.Row([
                dbc.Col(id='box-plot')
            ])
        ])
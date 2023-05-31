from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import metrics_experiment
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
                dbc.Col(width=5),
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
    # Total df
    all, all_mg = metrics_experiment.calculate_all_metrics(df_id, 
                        #ID='blob', units=i['Units'], 
                        additional_tirs=additional_tirs, lv1_hypo=lv1_hypo, 
                        lv2_hypo=lv2_hypo, lv1_hyper=lv1_hyper, 
                        lv2_hyper=lv2_hyper, event_mins=short_mins, event_long_mins=long_mins)
    # mmol
    all['period'] = 'All'
    all['units'] = 'mmol/L'
    all_results = all_results.append(all)

    # mg
    all_mg['period'] = 'All'
    all_mg['units'] = 'mg/dL'
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
        
        # mg
        day_mg['period'] = 'Day'
        day_mg['units'] = 'mg/dL'
        
    else:
        day = pd.DataFrame({'period':['Day'], 'units':['mmol/L']})
        day_mg = pd.DataFrame({'period':['Day'], 'units':['mg/dL']})

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
        
        # mg
        night_mg['period'] = 'Night'
        night_mg['units'] = 'mg/dL'
    else:
        night = pd.DataFrame({'period':['Night'], 'units':['mmol/L']})
        night_mg = pd.DataFrame({'period':['Night'], 'units':['mg/dL']})
    
    all_results = all_results.append(day)
    all_results = all_results.append(day_mg)
    all_results = all_results.append(night)
    all_results = all_results.append(night_mg)
    return all_results

def replace_cutoffs(dict, lo_cutoff, hi_cutoff, lo_hi_cutoff_checklist):
    df = pd.DataFrame(dict)
    if not 1 in lo_hi_cutoff_checklist:
        df['glc']= pd.to_numeric(df['glc'].replace({'High': lo_cutoff, 'Low': lo_cutoff, 'high': hi_cutoff, 'low': lo_cutoff, 
                             'HI':hi_cutoff, 'LO':lo_cutoff, 'hi':hi_cutoff, 'lo':lo_cutoff}))

        if 2 in lo_hi_cutoff_checklist:
            df['glc'][df['glc']>hi_cutoff] = hi_cutoff
            df['glc'][df['glc']<lo_cutoff] = lo_cutoff

    df = df[pd.to_numeric(df['glc'], errors='coerce').notnull()]
    df['glc'] = pd.to_numeric(df['glc'])
    df['time'] = pd.to_datetime(df['time'])
    df = df.reset_index(drop=True)
    return df


def calculate_metrics(processed_data, day_start, day_end, night_start, 
                            night_end, additional_tirs, lv1_hypo, lv2_hypo,
                            lv1_hyper, lv2_hyper, short_mins, long_mins,
                            lo_cutoff, hi_cutoff, lo_hi_cutoff_checklist): #
    # Breakdown df into night and day
    #processed_data = pd.DataFrame(processed_data)
    processed_data = replace_cutoffs(processed_data, lo_cutoff, hi_cutoff, lo_hi_cutoff_checklist)
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
import pandas as pd
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import base64
import io
import metrics_experiment
import metrics_helper
from datetime import timedelta
import datetime
import numpy as np
import section_metrics_tbl

poi_template = pd.DataFrame([['ID must match your IDs in the webapp', 
                              'dd/mm/yy/ HH:MM', 'dd/mm/yy/ HH:MM',	
                              'This can be used to label repeating periods']],
                              columns= ['ID', 'startDateTime', 'endDateTime', 'label'])

def create_period_of_interest():
    return html.Div([
        dbc.Row([
            dbc.Col(
                html.H2('Exploring specific periods of interest')
            ),
            dbc.Col(
                dbc.Alert(
                    [
                        html.I(className="bi bi-info-circle-fill me-2"),
                        'This section enables you to take a more in depth look at \
                            different periods of interest in your data. For more info \
                                and examples see instructions'
                    ],
                    color="info",
                    className="d-flex align-items-center")
            )
        ]),
        dbc.Card(dbc.CardBody([
            html.H4('1.Upload external data'),
            dbc.Collapse([
                html.P('For this to work you\'ll need to upload a file that includes the ID of the participant, the start and end times of the period \
                    of interest and an optional label.'),
                dcc.Upload(children=html.Div(
                        [
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },id='upload-poi-data',),
                html.Div(id='poi-datafile'),
        ], is_open=True),
        ])),

        dbc.Card(dbc.CardBody([
            html.H4('2. Select windows around events'),
            dbc.Collapse([
                html.P("Use the sliders and buttons below to select time period that you're \
                            interested in. The default is set to calculate the period of interest only \
                                but alongside this you can add periods before or after."),
                dbc.Accordion([
                    dbc.AccordionItem([
                        html.Div(id='poi-sliders'),
                        dbc.Button("Add another range", id='add-poi-slider', color='primary'),
                    ], title='Specific number of hours around event'),
                    dbc.AccordionItem([
                        html.P('Select the periods you\'re interested in around the event'),
                        dbc.Checklist(options=[{'label':'All 24hrs after event', 'value':1},
                                        {'label':'Night after event','value':2}], 
                                        id='set-periods-poi-checklist', value=[]),
                    ], title='Set periods around event'),
                ], start_collapsed=True),
                dbc.Row(dbc.Button('Calculate metrics', color="secondary", id='periodic-metrics-button',)),
            ], id='poi-2-collapse', is_open=False),
        ])),
        
        dbc.Card(dbc.CardBody([
            html.H4('3. Calculate metrics'),
            dbc.Collapse([
                dbc.Row([
                    dbc.Col(width=8),
                    dbc.Col([
                        dbc.RadioItems(
                            id="poi-unit-options",
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
                    ]),
                    
                ]),
                html.Div(dbc.Spinner(spinner_style={"width": "3rem", "height": "3rem"}), 
                            style={'textAlign':'center'}, id='poi-metrics')
            ],id='poi-collapse-3', is_open=False)
            ])),
    ])

def create_range_slider(n_clicks, children):
    id = 'poi-'+str(n_clicks)
    slider_id = id+'-slider'
    heading_id = id+'-heading'
    button_id = id+'-button'
    new_slider = dcc.RangeSlider(-14, 14, value=[-2, 2], marks={
            -2:{'label': 'Start of event'},
            2:{'label': 'End of event'},
            -6: {'label': '4hrs before'},
            -14: {'label': '12hrs before'},
            6: {'label': '4hrs after'},
            14: {'label': '12hrs after'},
            3:{}, 4:{}, 5:{}, 7:{}, 8:{}, 9:{}, 10:{}, 11:{}, 12:{}, 13:{}, #15:{}, 16:{},
            -3:{}, -4:{}, -5:{}, -7:{}, -8:{}, -9:{}, -10:{}, -11:{}, -12:{}, -13:{}, #-15:{}, -16:{},
            }, id=slider_id
        ),
    section = html.Div(dbc.Card([dbc.CardBody([
                    html.H6(id=heading_id),
                    dbc.Row([
                        dbc.Col(
                            new_slider
                        ),
                        dbc.Col([
                            dbc.Button('Remove', color="danger", id=button_id),
                        ], width=2)
                    ])]),
                ]), id=id)
    if children is not None:
        children.append(section)
        return children
    else:
        return [section]

def add_time_to_date(date, minutes):
    datetime = date + timedelta(minutes=minutes)
    return datetime

def combine_date_and_time(date, time):
    dt = datetime.datetime.combine(date, time)
    return dt

def standardise_poi_df(df):
    cols = df.columns
    if 'ID' in cols: 
        if set(['start_date', 'start_time']).issubset(cols):
            df['start_datetime'] = df.apply(lambda row: combine_date_and_time(row['start_date'],
                                                                              row['start_time']), axis=1)
            df = df.drop(columns=['start_date','start_time'])
            cols = df.columns

        if set(['end_date', 'end_time']).issubset(cols):
            df['end_datetime'] = df.apply(lambda row: combine_date_and_time(row['end_date'],
                                                                              row['end_time']), axis=1)
            df = df.drop(columns=['end_date','end_time'])
            cols = df.columns

        if set(['start_datetime', 'duration']).issubset(cols):
            df['end_datetime'] = df.apply(lambda row: add_time_to_date(row['start_datetime'], row['duration']), axis=1)
            df = df.drop(columns=['duration'])
            cols = df.columns

        if set(['start_datetime', 'end_datetime']).issubset(cols):
            df = df.rename(columns={'start_datetime':'Start of event', 'end_datetime':'End of event'})
            df = df.set_index(['ID', 'Start of event', 'End of event']).reset_index()
            return df
        else:
            return None
    else:
        return None

def parse_file(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
        standardised_df = standardise_poi_df(df)
        if standardised_df is not None:
            return standardised_df.to_dict('records')
        else:
            return 'columns'

    except Exception as e:
        print(e)
        return 'format'

def drag_values(drag):
    if drag[0]>=-2 and drag[0]<0:
        first_num = 'start'
        first = 'Start of event'
    elif drag[0]>0 and drag[0]<=2:
        first_num = 'end'
        first = 'End of event'
    elif drag[0]<-2:
        first_num= np.round(drag[0]+2, 2)
        if abs(first_num) == 1:
            first = f'{abs(first_num)}hr before'
        else:
            first = f'{abs(first_num)}hrs before'
    elif drag[0]>2:
        first_num= np.round(drag[0]-2, 2)
        if first_num == 1:
            first = f'{first_num}hr after'
        else:
            first = f'{first_num}hrs after'
    if drag[1]>=-2 and drag[1]<0:
        last_num = 'start'
        last = 'start of event'
    elif drag[1]>0 and drag[1]<=2:
        last_num = 'end'
        last = 'end of event'
    elif drag[1]<-2:
        last_num = np.round(drag[1]+2, 2)
        if abs(last_num) == 1:
            last = f'{abs(last_num)}hr before'
        else:
            last = f'{abs(last_num)}hrs before'
    elif drag[1]>2:
        last_num = np.round(drag[1]-2, 2)
        if last_num == 1:
            last = f'{last_num}hr after'
        else:
            last = f'{last_num}hrs after'
    return first, last, first_num, last_num

def get_drag_times(first_num, last_num, start, end):
    if first_num=='start':
        first_time = start
    elif first_num =='end':
        first_time = end
    elif first_num>0:
        first_time = end+timedelta(hours=first_num)
    else:
        first_time = start-timedelta(hours=abs(first_num))
    # Last num value
    if last_num=='start':
        last_time = start
    elif last_num =='end':
        last_time = end
    elif last_num>0:
        last_time = end+timedelta(hours=float(last_num))
    else:
        last_time = start-timedelta(hours=float(abs(last_num)))
    return first_time, last_time

def periodic_calculations(info, glc_data, id_raw_data, first_time, 
                          last_time, start, end, additional_tirs, 
                          lv1_hypo, lv2_hypo, lv1_hyper, lv2_hyper, 
                          short_mins, long_mins):

    sub_df = glc_data[(glc_data['time']>=first_time)&(glc_data['time']<last_time)]
    
    if sub_df.empty:
        info['Data Sufficiency (%)'] = 0
        info_mg = info.copy()
        info['units'] = 'mmol/L'
        info_mg['units'] = 'mg/dL'
        return info, info_mg
        
    else:
        data_sufficiency = metrics_helper.helper_missing(sub_df, 
                                                            gap_size=id_raw_data['Interval'], 
                                                            start_time=first_time, 
                                                            end_time=last_time)['Data Sufficiency (%)']
        info['Data Sufficiency (%)'] = data_sufficiency
        info_mg = info.copy()
        metrics, metrics_mg = metrics_experiment.calculate_all_metrics(sub_df, return_df=False, 
                        #units=id_raw_data['Units'], #interval=id_raw_data['Interval'], 
                        additional_tirs=additional_tirs, lv1_hypo=lv1_hypo, 
                        lv2_hypo=lv2_hypo, lv1_hyper=lv1_hyper, lv2_hyper=lv2_hyper, 
                        event_mins=short_mins, event_long_mins=long_mins
                        )
        if metrics is None:
            info['Data Sufficiency (%)'] = 0
            info_mg = info.copy()
            info['units'] = 'mmol/L'
            info_mg['units'] = 'mg/dL'
            return info, info_mg

        metrics['units'] = 'mmol/L'
        metrics_mg['units'] = 'mg/dL'
        info.update(metrics)
        info_mg.update(metrics_mg)
        return info, info_mg
    

def calculate_periodic_metrics(poi_ranges, set_periods, poi_data, raw_data, 
                               additional_tirs, lv1_hypo, lv2_hypo, lv1_hyper, 
                               lv2_hyper, short_mins, long_mins, night_start, 
                               night_end, low_cutoff, high_cutoff, checklist):
    results = []
    
    for i in poi_data:
        ID = i['ID']
        start_event =  pd.to_datetime(i['Start of event']).round('S')
        end_event = pd.to_datetime(i['End of event']).round('S')
        info = {'ID':ID, 'Start of event':start_event, 
                'End of event':end_event, 'Period':'CGM file not available'}
        info_mg = info.copy()
        info['units'] = 'mmol/L'
        info_mg['units'] = 'mg/dL'

        try:
            id_raw_data = next(item for item in raw_data if item['ID'] == ID)
        except:
            ##### Add sumink #####
            results.append(info)
            results.append(info_mg)
            continue
        if not id_raw_data['Usable']:
            # Return ID with sumink or uvver
            results.append(info)
            results.append(info_mg)
            continue
        glc_data = pd.DataFrame.from_dict(id_raw_data['data'])
        glc_data['time'] = pd.to_datetime(glc_data['time'])
        
        # Replace lo/hi values
        glc_data = section_metrics_tbl.replace_cutoffs(glc_data, low_cutoff, 
                                                     high_cutoff, checklist)

        for drag in poi_ranges:
            # First num values
            first, last, first_num, last_num = drag_values(drag)
            first_time, last_time = get_drag_times(first_num, last_num, 
                                                   start_event, end_event)

            info_drag = info.copy()
            info_drag['Period'] = f'{first} to {last}'
            metrics, metrics_mg = periodic_calculations(info_drag, glc_data, id_raw_data, 
                                                        first_time, last_time, start_event, 
                                                        end_event, additional_tirs, lv1_hypo, 
                                                        lv2_hypo, lv1_hyper, lv2_hyper, 
                                                        short_mins, long_mins) 
            
            results.append(metrics)
            results.append(metrics_mg)

        
        if 1 in set_periods:
            info_24 = info.copy()
            info_24['Period'] = f'24hrs after'
            first_time = end_event
            last_time = end_event + timedelta(hours=24)
            metrics, metrics_mg = periodic_calculations(info_24, glc_data, id_raw_data,
                                                        first_time, last_time, start_event,
                                                        end_event,additional_tirs, lv1_hypo, 
                                                        lv2_hypo, lv1_hyper, lv2_hyper,
                                                        short_mins, long_mins) 
            results.append(metrics)
            results.append(metrics_mg)
        
        
        if 2 in set_periods:
            info_eve = info.copy()
            info_eve['Period'] = f'Night after event'
            night_start_minutes = int(night_start[14:16])
            night_start_hours = int(night_start[11:13])

            first_time = start_event.replace(hour=night_start_hours, minute=night_start_minutes)
            if night_start_hours<12:
                first_time += timedelta(hours=24)

            night_end_minutes = int(night_end[14:16])
            night_end_hours = int(night_end[11:13])
            last_time = start_event.replace(hour=night_end_hours, minute=night_end_minutes)
            if night_end_hours<12:
                last_time += timedelta(hours=24)
    
            metrics, metrics_mg = periodic_calculations(info_eve, glc_data, id_raw_data,
                                                        first_time, last_time, start_event,
                                                        end_event,additional_tirs, lv1_hypo, 
                                                        lv2_hypo, lv1_hyper, lv2_hyper,
                                                        short_mins, long_mins) 
            results.append(metrics)
            results.append(metrics_mg)
    all_metrics = pd.DataFrame.from_dict(results)
    poi_data = pd.DataFrame.from_dict(poi_data)
    poi_data['Start of event'] = pd.to_datetime(poi_data['Start of event'])#.round('S')
    poi_data['End of event'] = pd.to_datetime(poi_data['End of event'])#.round('S')

    merged_results = pd.merge(poi_data, all_metrics, how='left', 
                              on=['ID', 'Start of event', 'End of event'])
    return merged_results.to_dict('records')

def create_data_table(data):
    df = pd.DataFrame.from_dict(data).round(2)
    df['Start of event'] = pd.to_datetime(df['Start of event']).astype(str)
    df['End of event'] = pd.to_datetime(df['End of event']).astype(str)
    df = df.fillna('N/A')
    return dash_table.DataTable(id='poi-data', data=df.to_dict('records'), 
                columns=[
                        {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                        if i == "iso_alpha3" or i == "ID" or i == "id"
                        else {"name": i, "id": i, "hideable": True, "selectable": True}
                        for i in df.columns
                ],
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
                    'maxHeight': '40vh',
                    },
                
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    #'fontWeight': 'bold'
                },
                #editable=True,              # allow editing of data inside all cells                        
                filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                export_format="csv",
                export_headers="display",
                column_selectable='multi',
                #fixed_rows={'headers':True},
                fill_width=False,
                tooltip_header={
                        'LBGI':'Low blood glucose index',
                        'HBGI': 'High blood glucose index',
                        'AUC (mmol h/L)': 'Average hourly area under the curve',
                        
                    },
)


import pandas as pd
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import base64
import io
import metrics_experiment
from datetime import timedelta


poi_template = pd.DataFrame([['ID must match your IDs in the webapp',	'dd/mm/yy/ HH:MM',	'dd/mm/yy/ HH:MM',	'This can be used to label repeating periods']], columns= ['ID', 'startDateTime', 'endDateTime', 'label'])
accordion = dbc.Accordion(
            [dbc.AccordionItem(
                    [
                        html.P("This section will be for diet")
                    ],
                    title="Diet",
                ),
                dbc.AccordionItem(
                    [
                        html.P("This section will be for insulin data")
                    ],
                    title="Insulin",
                ),
                dbc.AccordionItem(
                    [
                        html.P("This section will be for exercise")
                    ],
                    title="Exercise",
                ),
                dbc.AccordionItem(
                    [html.H5('File template'),
                    dash_table.DataTable(data=poi_template.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in poi_template.columns],
                                export_format="csv",
                                export_headers="display",
                                style_table={'overflowX': 'auto',},
                                style_cell={'whiteSpace': 'normal',},),
                    dcc.Upload(dbc.Button('Upload periods file', color="secondary"),
                                multiple=False,
                                id='upload-poi-data',),
                    html.Div(id='poi-datafile'),
                    html.H5('Time after period'),
                    dcc.Checklist(['1 hour', '2 hours', '3 hours', '4 hours'], id='time-after-checklist', inline=False),
                                ],
                    title="Other",
                ),
])

def create_period_of_interest():
    return html.Div([
        html.H2('Incorporating external factors'),
        html.P('This section enables you to take a more in depth look at different periods of interest in your data. \
            For this to work you\'ll need to upload a file that includes the ID of the participant, the start and end times of the period \
            of interest and an optional label. From there, you\'ll get a breakdown of the metrics of glycemic control\
            for all of the periods you\'ve entered.\
            For this part you need to pay close attention to the INSTRUCTIONS because there\'s lots of ways to mess this up. Good luck brave warrior.'),
        
        dbc.Card(dbc.CardBody([
            html.H4('1.Upload external data'),
            html.P('For this to work you\'ll need to upload a file that includes the ID of the participant, the start and end times of the period \
            of interest and an optional label.'),
            dcc.Upload(dbc.Button('Upload file', color="secondary"),
                            multiple=False, id='upload-poi-data',),
            html.Div(id='poi-datafile'),
        ])),
        dbc.Card(dbc.CardBody([
            html.H4('2. Select analysis options'),
            html.P("Use the slider below to select time period that you're interested in. \
                                        The default is set to calculate the period of interest only \
                                            but alongside this you can add periods before or after."),
            dbc.Row([
                dbc.Col([#dbc.Card([dbc.CardBody([
                    #html.H5('Number of hours after analysis'),
                    html.Div(id='poi-sliders'),
                    dbc.Button("Add another range", id='add-poi-slider', color='primary'),
                ]),#])]),
                dbc.Col([dbc.Card([dbc.CardBody([
                    html.H5('Day/night calculations'),
                    dbc.Checklist(options=[{'label':'Days with events', 'value':1}, {'label':'Days without events','value':2}, 
                                    {'label':'Nights after events','value':3}, {'label':'Nights after no events','value':4}], 
                                    id='day-night-poi-checklist', value=[]),
                ])])], width=3)
            ])
        ])),
        dbc.Card(dbc.CardBody([
            html.H4('3. Calculate metrics'),
            dbc.Button('Calculate', color="secondary", id='periodic-metrics-button',),
            html.Div(id='poi-metrics')
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
        if set(['ID', 'startDatetime', 'endDatetime', 'label']).issubset(df.columns):
            return df.to_dict('records')
        else:
            return html.Div(['Columns are incorrect'])

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing file with name: ' + filename
        ])

def calculate_periodic_metrics(poi_data, raw_data, additional_tirs, lv1_hypo, lv2_hypo, lv1_hyper, lv2_hyper, short_mins, long_mins, day_start, day_end, night_start, night_end, hours_after=4):
    results = []
    for i in poi_data:
        ID = i['ID']
        start = pd.to_datetime(i['startDatetime']).round('S')
        end = pd.to_datetime(i['endDatetime']).round('S')
        label = i['label']
        try:
            id_raw_data = next(item for item in raw_data if item["ID"] == ID)
        except:
            # Add sumink
            continue
        #raw_data = pd.DataFrame.from_dict(raw_data)
        #id_raw_data = raw_data[raw_data['ID']==ID]
        if not id_raw_data['Usable']:
            # Return ID with sumink or uvver
            continue
        glc_data = pd.DataFrame.from_dict(id_raw_data['data'])
        glc_data['time'] = pd.to_datetime(glc_data['time'])
        subsection = glc_data[(glc_data['time']>=start)&(glc_data['time']<end)]
        #subsection = [i for i in glc_data if ((i['time']>=start)&(i['time']<=end))]
        df = subsection #pd.DataFrame.from_dict(subsection)
        if df.empty:
            # Should probs add something here
            continue
        else:
            metrics, metrics_mg = metrics_experiment.calculate_all_metrics(df, return_df=False, #ID=ID, 
                                    units=id_raw_data['Units'], #interval=id_raw_data['Interval'], 
                                    additional_tirs=additional_tirs, lv1_hypo=lv1_hypo, 
                                    lv2_hypo=lv2_hypo, lv1_hyper=lv1_hyper, lv2_hyper=lv2_hyper, 
                                    event_mins=short_mins, event_long_mins=long_mins
                                    )
            #info = pd.DataFrame([[ID, label, 'During', start, end]], columns = ['ID', 'Label', 'Period', 'startDatetime', 'endDatetime'])
            info = {'ID':ID, 'Label':label, 'Period': 'During', 'startDatetime':start, 'endDatetime':end}
            metrics_mg['label'] = label
            info.update(metrics)
            #combined = pd.concat([info, metrics], axis=1)
            results.append(info)
            #results.append(combined)

            
            for j in range(0, hours_after):
                print(j)
                start = end+timedelta(hours=j)
                end = end+timedelta(hours=j+1)
                
                df = glc_data[(glc_data['time']>=start)&(glc_data['time']<end)]
                info = {'ID':ID, 'Label':label, 'Period': f'{j+1} hour after', 'startDatetime':start, 'endDatetime':end}
                print(info)
                if df.empty:
                    #continue
                    results.append(info)
                else:
                    metrics, metrics_mg = metrics_experiment.calculate_all_metrics(df, ID=ID, 
                                    units=id_raw_data['Units'], #interval=id_raw_data['Interval'], 
                                    additional_tirs=additional_tirs, lv1_hypo=lv1_hypo, 
                                    lv2_hypo=lv2_hypo, lv1_hyper=lv1_hyper, lv2_hyper=lv2_hyper, 
                                    event_mins=short_mins, event_long_mins=long_mins
                                    )
                    #info = {'ID':ID, 'Label':label, 'Period': f'{j+1} hour after', 'startDatetime':start, 'endDatetime':end}
                    #metrics_mg['label'] = label
                    info.update(metrics)
                    results.append(info)

    return results

def create_data_table(data):
    df = pd.DataFrame.from_dict(data).round(2)
    df['startDatetime'] = df['startDatetime'].astype(str)
    df['endDatetime'] = df['endDatetime'].astype(str)

    return html.Div([
        dbc.RadioItems(
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
        dash_table.DataTable(id='poi-data', data=df.to_dict('records'), 
            columns=[
                            {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                            if i == "iso_alpha3" or i == "ID" or i == "id"
                            else {"name": i, "id": i, "hideable": True, "selectable": True}
                            for i in df.columns
                ],
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
                export_format="csv",
                export_headers="display",
                column_selectable='multi',
                fill_width=False,
                tooltip_header={
                        'LBGI':'Low blood glucose index',
                        'HBGI': 'High blood glucose index'

                    },
                )
    ])


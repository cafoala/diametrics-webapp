from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import metrics_experiment
import periods

def calculate_metrics(raw_data):
    all_results = []
    #day_results = []
    #night_results = []

    for i in raw_data:
        if i['Usable']==True:
            df_id = pd.DataFrame.from_dict(i['data'])
            df_id.time = pd.to_datetime(df_id.time)
            # Total df
            all = metrics_experiment.calculate_all_metrics(df_id, ID=i['ID'], unit=i['Units'], interval=i['Interval'])
            all['period'] = 'All'
            all_results.append(all)

            # Breakdown df into night and day
            df_day, df_night = periods.get_day_night_breakdown(df_id)
            
            # Daytime breakdown metrics 
            day= metrics_experiment.calculate_all_metrics(df_day, ID=i['ID'], unit=i['Units'], interval=i['Interval'])
            day['period'] = 'Day'
            #day_results.append(day)
            all_results.append(day)

            
            # Night breakdown metrics
            night= metrics_experiment.calculate_all_metrics(df_night, ID=i['ID'], unit=i['Units'], interval=i['Interval'])
            night['period'] = 'Night'
            #night_results.append(night)
            all_results.append(night)
    return all_results
        
def create_metrics_table(df):    
    return dash_table.DataTable(
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
                export_format="csv",
                export_headers="display",
                column_selectable='multi',
                fill_width=False
                )

def get_metrics_layout():
    units = dcc.RadioItems(
                ['mmol/L', 'mg/dL'],
                'mmol/L ',
                id='unit-type',
                inline=True
            ),
    time_period = dcc.RadioItems(
                ['All', 'Day', 'Night'],
                'All',
                id='period-type',
                inline=True
            )
    
    metrics_layout = html.Div([
        dbc.Row([
                    dbc.Col(html.H2('Metrics of Glycemic Control')),
                    dbc.Col(units),
                    dbc.Col(time_period),
        ]),
        dbc.Row([
                dbc.Col(id='test-table'),
                ]),
    ])
    return metrics_layout
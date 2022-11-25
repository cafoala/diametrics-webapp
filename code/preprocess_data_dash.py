@app.callback([Output('raw-data-store', 'data'),
    Output('data-tbl', 'children'),],
    Input('preprocess-button', 'n_clicks'),
    State('upload-data', 'last_modified'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True)
def preprocess_data(n_clicks, list_of_dates, list_of_contents, list_of_names):
    #if n_clicks is not None:
    #    n_clicks = 0
    if n_clicks is None or list_of_dates is None:
        raise PreventUpdate
    if n_clicks >0:
        print('preprocessing')
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        
        #dcc.Store(storage_type='local', id='raw-data-store', data=children),#.to_dict('records')),                    

        data_details = pd.DataFrame.from_dict(children)[['Filename', 'ID', 'Usable', 'Device', 'Interval', 'Data Sufficiency', 'Start Time', 'End Time']]
        data_table = html.Div([
                html.H2('Data details'),

                dash_table.DataTable(
                    id='data_tbl',
                    columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                                if i == "iso_alpha3" or i == "Filename" or i == "id"
                                else {"name": i, "id": i, "hideable": True, "selectable": True}
                                for i in data_details.columns
                    ],
                    data=data_details.to_dict('records'),
                    style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                #'width':'200px'
                            },
                    
                    style_table={
                        'overflowX': 'auto',
                        #'height': 300,
                        },
                    editable=True,              # allow editing of data inside all cells
                    filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                    sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                    export_format="csv",
                    export_headers="display",
                    ),
                    html.P('The table shows your preprocessed data. Please make sure to check that the data is \
                        what you want for your files and edit accordingly. Most importantly, the ID, the start and \
                            end dates as these will be used for the rest of your data analysis. If you do edit, \
                                please press the reprocess button to get an updated table'),
                    dbc.Button('Calculate metrics', id='calculate-metrics', color='secondary')
            ]),
            
        collapse_table = html.Div([
                dbc.Button("Your Data", color="primary", id="collapse-data-tbl-button", n_clicks=0),
                dbc.Row([
                    dbc.Collapse(
                        dbc.Card(data_table, body=True),
                        id="data-tbl-collapse",
                        is_open=True,
                    )
            ]),
        ])
        return (children, collapse_table)

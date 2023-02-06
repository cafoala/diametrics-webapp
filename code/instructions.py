'''dbc.Button('Instructions', id='instruction-button'),
        dbc.Collapse(dbc.Card(dbc.CardBody([
            html.P('1. Create an excel or csv file with headers shown in the template below or download the template using the export button'),
            #
            dash_table.DataTable(data=poi_template.to_dict('records'),
                        columns=[{"name": i, "id": i} for i in poi_template.columns],
                        export_format="csv",
                        export_headers="display",
                        style_table={'overflowX': 'auto',},
                        style_cell={'whiteSpace': 'normal',},),
            html.P('2. Fill in the IDs, must match with the ones in your processed data (table in above section)'),
            html.P('3. The start and end time of the period must be in the format DD/MM/YY HH:MM'),
            html.P('4. Add a label if you\'d like to'),
            html.P('5 Add an optional set period to look at the window after your period of interest'),
        ])), id='instructions-collapse'),'''
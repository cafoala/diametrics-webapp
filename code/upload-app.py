import base64
import datetime
import io
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import logging
import pandas as pd
import dash_bootstrap_components as dbc

import sys
sys.path.append("/Users/cr591/OneDrive - University of Exeter/Desktop/diametrics/diametrics")
import preprocessing
import metrics_experiment

logging.basicConfig(level=logging.DEBUG)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Frankenstein\'s App', style={
            'textAlign': 'center'}),
    html.Div(children='Where science meets desperation...', style={
            'textAlign': 'center'}),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'justify': "center",
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(
        id='output-data-upload',
        style={
            'width': '80%',
            'height': '60px',
            'textAlign': 'center',
            'margin': '10px'
        },
    ),
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), header=None)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded), header=None)

        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+', header=None)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing file with name: ' + filename
        ])
    return preprocessing.preprocess_df(df, filename)
    '''
    logging.debug(df[['Meter Timestamp', 'Historic Glucose(mmol/L)']].head())
    fig = px.line(df, x='Meter Timestamp', y='Historic Glucose(mmol/L)')
    


    return html.Div([
        html.H5(datetime.datetime.fromtimestamp(date)),
        
        html.Div([
            html.H6(filename),
            dash_table.DataTable(
                df.to_dict('records'),
                [{'name': i, 'id': i} for i in df.columns]),
            html.Hr()],
            id='table-to-hide', style={'display': 'block'}),
        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ], style={'display': 'block'})
    '''


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        
        dict_results = []
        for i in children:
            if i.usable==True:
                df_id = i.data
                results = metrics_experiment.calculate_all_metrics(df_id, ID=i.id, unit=i.units, interval=i.interval)
                dict_results.append(results)
        metrics = pd.DataFrame.from_dict(dict_results).round(2)


        return html.Div([
            #html.H5(datetime.datetime.fromtimestamp(date)),
            
            html.Div([
                html.H6('Metrics of Glycemic Control'),
                dash_table.DataTable(
                    data=metrics.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in metrics.columns],
                    style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                'width':'200px'
                            },
                    style_table={'overflowX': 'auto'},
                    style_cell={
                                'height': 'auto',
                                # all three widths are needed
                                'minWidth': '70px', 'width': '95px', 'maxWidth': '120px',
                                'lineHeight': '10px',
                                'whiteSpace': 'normal'
                            },
                    ),
                html.Hr()],
                id='tbl', style={'display': 'block'}),
                
                dcc.Graph(
                    id='example-graph',
                    figure=px.bar(metrics, x='ID', y='Average glucose')
            )
        ], style={'display': 'block'})

'''
@app.callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"
    '''

if __name__ == '__main__':
    app.run_server(debug=True)

### Run with pytest don't ask why
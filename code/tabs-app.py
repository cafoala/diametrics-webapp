import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import logging
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate
import layout

# Import modules with section contents
import section_upload_content
import section_data_tbl
import section_analysis_options
import section_metrics_tbl
import section_overview_figs
import section_individual_figs
logging.basicConfig(level=logging.DEBUG)

external_stylesheets = [dbc.themes.JOURNAL]
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#, suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True

upload_section= dbc.Card(
    dbc.CardBody([
        dbc.Row([
                dbc.Col(html.Div([
                    html.H2('Upload files'),
                    html.P('To begin, use the button to select your CGM files'),
                    ]
                #style={'textAlign': 'left'}
                ), width=8),
                dbc.Col(dcc.Upload(dbc.Button('Select Files', color="secondary"),
                                multiple=True,
                                id='upload-data',))
        ]),
        dbc.Row([
                dbc.Col(html.Div(id='filelist'))
            ]),
    ])  
),
#upload_section = section_upload_content.get_upload_layout()

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)



app.layout = html.Div([
                dbc.Tabs(
                    [
                        dbc.Tab(section_upload_content.get_upload_layout(), label="1. Upload files", tab_id="upload-tab", id='upload-tab', active_label_style={"color": "#FB79B3"}),
                        dbc.Tab(section_data_tbl.get_datatable_layout(), label="2. Check data", tab_id="data-tab",id="data-tab", disabled=True, active_label_style={"color": "#FB79B3"}),
                        dbc.Tab(section_analysis_options.get_analysis_options_layout(), label="3. Analysis options", tab_id="other-metrics-tab", id='other-metrics-tab', disabled=False, active_label_style={"color": "#FB79B3"}),
                        dbc.Tab(section_metrics_tbl.get_metrics_layout(), label="4. Standard metrics", tab_id="metrics-tab", id='metrics-tab', disabled=False, active_label_style={"color": "#FB79B3"}),
                        dbc.Tab(label="5. Incorporating external factors", tab_id="poi-tab", id='poi-tab', disabled=True, active_label_style={"color": "#FB79B3"}),
                    ],
                    id="card-tabs",
                    active_tab="upload-tab",
                )
])
app.layout = layout.create_tabs_layout()

@app.callback(Output('other-metrics-tab', 'disabled'),
        Output('poi-tab', 'disabled'),
        Output('metrics-tab', 'disabled'),
        #Output('card-tabs', 'active_tab'),
        Input('calculate-metrics-button', 'n_clicks'))
def show_all_tabs(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return False, #'metrics-tab'

@app.callback(Output('data-tab', 'disabled'),
Output('card-tabs', 'active_tab'),
Input('preprocess-button', 'n_clicks')
)
def show_next_tab(n_clicks):    
    if n_clicks is None:
        raise PreventUpdate
    return False, 'data-tab'

@app.callback(Output("card-content", "children"), [Input("card-tabs", "active_tab")])
def switch_tab(at):
    print(at)
    if at == "upload-tab":
        return upload_section
    elif at == "data-tab":
        return section_data_tbl.get_datatable_layout()
    elif at == "metrics-tab":
        return section_metrics_tbl.get_metrics_layout()
    elif at == 'other-metrics-tab':
        return section_analysis_options.get_analysis_options_layout()
    return html.P("Empty page alert!")


# CALLBACKS # 

## FILELIST ## 
# List the filenames
@app.callback(Output('filelist', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
    prevent_initial_call=True)
def list_files(list_of_contents, list_of_names):
    if list_of_contents is not None:

        file_list = section_upload_content.create_file_list(list_of_names)
        return file_list#, False

if __name__ == '__main__':
    app.run_server(debug=True)#, dev_tools_ui=False)

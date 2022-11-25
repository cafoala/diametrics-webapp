from dash import dcc, html, dash_table
import plotly.express as px
#import statsmodels
import pandas as pd

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

def create_bargraph(df, y_axis):
    return html.Div([
        
        dcc.Graph(
                id='bargraph',
                figure=px.bar(df, x='ID', y=y_axis)
        )
    ])

def create_boxplot(df, y_axis):
    return html.Div([
        dcc.Graph(
                id='boxplot',
                figure=px.box(df, y=y_axis)
    )
    ])

def create_scatter(df, x_axis, y_axis):
    fig=px.scatter(df, x=x_axis, y=y_axis, trendline="ols")
    scatter = html.Div([
        dcc.Graph(
                id='scatterplot',
                figure=fig)
    ])

    results = px.get_trendline_results(fig)
    results_as_html = results.px_fit_results.iloc[0].summary().as_html()
    stats_df = pd.read_html(results_as_html, header=0, index_col='None')[0]    
    stats = html.Div([
        dash_table.DataTable(
            id='summarystats',
            data=stats_df.to_dict('records'),
        )
    ])
    return scatter, stats


def create_glucose_trace(df): 
    return html.Div([
            dcc.Graph(
                        id='line-graph',
                        figure=px.line(df, x='time', y='glc')
            )
    ])

def create_amb_glc_profile(df):
    
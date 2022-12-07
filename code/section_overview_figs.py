from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd

def create_bargraph(df, y_axis):
    if y_axis=='Time in range':
        fig = px.bar(df, x='ID', y=['TIR level 2 hypoglycemia', 'TIR level 1 hypoglycemia', 'TIR normal', 'TIR level 1 hyperglycemia', 'TIR level 2 hyperglycemia'])
    elif y_axis =='Hypoglycemic episodes':
        fig = px.bar(df, x='ID', y=['Level 1 hypoglycemic episodes', 'Level 2 hypoglycemic episodes'])
    elif y_axis == 'LBGI/HBGI':
        fig = px.bar(df, x='ID', y=['LBGI', 'HBGI'])
    else:
        fig = px.bar(df, x='ID', y=y_axis)
    return html.Div([
        dcc.Graph(
                id='bargraph',
                figure=fig
    )
    ])


def create_boxplot(df, y_axis):
    if y_axis=='Time in range':
        y_value=['TIR level 2 hypoglycemia', 'TIR level 1 hypoglycemia', 'TIR normal', 'TIR level 1 hyperglycemia', 'TIR level 2 hyperglycemia']
    elif y_axis =='Hypoglycemic episodes':
        y_value=['Hypoglycemic episodes', 'Level 1 hypoglycemic episodes', 'Level 2 hypoglycemic episodes']
    elif y_axis == 'LBGI/HBGI':
        y_value=['LBGI', 'HBGI']
    else:
        y_value=y_axis

    fig = px.box(df, y=y_value, points="all")
    return html.Div([
        dcc.Graph(
                id='boxplot',
                figure=fig
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
    stats_df = pd.read_html(results_as_html, header=0, index_col=0)[0]    
    stats = html.Div([
        dash_table.DataTable(
            id='summarystats',
            data=stats_df.to_dict('records'),
        )
    ])
    return scatter, stats
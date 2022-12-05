from dash import dcc, html, dash_table
import plotly.express as px
#import statsmodels
import pandas as pd
import numpy as np
import plotly.graph_objects as go


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
    if y_axis=='Time in range':
        fig = px.bar(df, x='ID', y=['TIR level 2 hypoglycemia', 'TIR level 1 hypoglycemia', 'TIR normal', 'TIR level 1 hyperglycemia', 'TIR level 2 hyperglycemia'])
    elif y_axis =='Hypoglycemic episodes':
        fig = px.bar(df, x='ID', y=['Level 1 hypoglycemic episodes', 'Level 2 hypoglycemic episodes'])
    elif y_axis == 'LBGI/HBGI':
        fig = px.bar(df, x='ID', y=['LBGI', 'HBGI'])
    else:
        fig = px.bar(df, y=y_axis)
    return html.Div([
        dcc.Graph(
                id='bargraph',
                figure=fig
    )
    ])
    '''
    return html.Div([
        
        dcc.Graph(
                id='bargraph',
                figure=px.bar(df, x='ID', y=y_axis)
        )
    ])'''

def create_boxplot(df, y_axis):
    if y_axis=='Time in range (all)':
        fig = px.box(df, x='ID', y=['TIR level 2 hypoglycemia', 'TIR level 1 hypoglycemia', 'TIR normal', 'TIR level 1 hyperglycemia', 'TIR level 2 hyperglycemia'])
    elif y_axis =='Hypoglycemic episodes':
        fig = px.box(df, x='ID', y=['Level 1 hypoglycemic episodes', 'Level 2 hypoglycemic episodes'])
    elif y_axis == 'LBGI/HBGI':
        fig = px.box(df, x='ID', y=['LBGI', 'HBGI'])
    else:
        fig = px.box(df, y=y_axis)
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
    print(results.head())
    results_as_html = results.px_fit_results.iloc[0].summary().as_html()
    stats_df = pd.read_html(results_as_html, header=0, index_col=0)[0]    
    stats = html.Div([
        dash_table.DataTable(
            id='summarystats',
            data=stats_df.to_dict('records'),
        )
    ])
    return scatter, stats


def create_glucose_trace(df): 
    fig = px.line(df, x='time', y='glc')
    fig.update_layout(
        title = 'Overall glucose trace',
        yaxis_title = 'Glucose (mmol/L)',
        xaxis_title = 'Date'
        )
    return html.Div([
            dcc.Graph(
                        id='line-graph',
                        figure=fig
            )
    ])

def create_amb_glc_profile(df):
    print(df.head())
    df.time = pd.to_datetime(df.time)
    grouped = df.set_index('time').groupby(pd.Grouper(freq='15min')).mean()['glc']
    group_frame = grouped.reset_index().dropna()
    amb_prof = group_frame.groupby(group_frame['time'].dt.time).apply(lambda group: pd.DataFrame([np.percentile(group.glc, [90, 75, 50, 25, 10])], columns=['q90', 'q3', 'q2', 'q1', 'q10'])).reset_index().drop(columns=['level_1'])

    # Set values for graph
    x = amb_prof['time'] #.astype(str)
    q2 = amb_prof['q2']
    q1 = amb_prof['q1']
    q3 = amb_prof['q3']
    q10 = amb_prof['q10']
    q90 = amb_prof['q90']

    tick_values = x[0::8]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x, y=q1,
        fill=None,
        line_color='rgb(0,176,246)',
        name='25-75%-IQR',
        ))
    fig.add_trace(go.Scatter(
        x=x,
        y=q3,
        fill='tonexty',
        fillcolor='rgba(0,176,246,0.1)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=x, y=q2,
        line_color='orange',
        name='50%-Median',
    ))
    fig.add_trace(go.Scatter(
        x=x,
        y=q3,
        line_color='rgb(0,176,246)',
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=x,
        y=q10,
        line_color='green',
        showlegend=True,
        line=dict(dash='dash'),
        name='10/90%',
    ))
    fig.add_trace(go.Scatter(
        x=x,
        y=q90,
        line_color='green',
        showlegend=False,
        line=dict(dash='dash'),
        name='10/90%',
    ))

    #fig.add_hrect(y0=3.9, y1=10, line_width=0, fillcolor="grey", opacity=0.2, name='Target range')
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_layout(
        title = 'Ambulatory glucose profile',
        yaxis_title = 'Glucose (mmol/L)',
        xaxis_title = 'Time (hr)',
        xaxis = dict(tickmode = 'array',
            tickvals = tick_values,
            ticktext = [i.strftime('%I %p') for i in tick_values])
    )

    return html.Div([
        dcc.Graph(
                id='amb-glc-prof',
                figure=fig)
    ])
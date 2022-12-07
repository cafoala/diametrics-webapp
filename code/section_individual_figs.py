from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

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
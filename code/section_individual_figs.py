from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
colors = ['blue', 'purple', 'grey', 'pink', 'red']
def create_indiv_layout():
    figs_layout = html.Div([
        html.H2('Closer look at individual participants'),
        html.Div(id='subject-id-div'),
        html.Div(dbc.Spinner(spinner_style={"width": "3rem", "height": "3rem"}), id='amb-glc-profile'),
        html.Div(id='pie-chart'),
        html.Div(id='glc-trace'),
    ])
    return figs_layout

def create_glucose_trace(df):
    fig = go.Figure()
    # Create and style traces
    fig.add_trace(go.Scatter(x=df.time, y=df.glc,
                            line=dict(color='black', ), 
                            opacity=0.5,
                            showlegend=False, name='Glucose trace'),
                            #row=1, col=1
                            )
    # Add shape regions
    fig.add_hrect(
        y0="0", y1="3",
        fillcolor=colors[0], opacity=0.2,
        layer="below", line_width=0,
        #row=1, col=1
    ),
    fig.add_hrect(
        y0="3", y1="3.9",
        fillcolor=colors[1], opacity=0.2,
        layer="below", line_width=0,
        #row=1, col=1
    ),
    fig.add_hrect(
        y0="3.9", y1="10",
        fillcolor=colors[2], opacity=0.2,
        layer="below", line_width=0,
        #row=1, col=1
    ),
    fig.add_hrect(
        y0="10", y1="13.9",
        fillcolor=colors[3], opacity=0.2,
        layer="below", line_width=0,#annotation_text='Level 1 hyperglycemia (10-13.9)', annotation_position="top left",
        #row=1, col=1
    ),
    fig.add_hrect(
        y0="13.9", y1="23",
        fillcolor=colors[4], opacity=0.2,
        layer="below", line_width=0,#annotation_text='Level 2 hyperglycemia (>13.9)', annotation_position="top left",
        #row=1, col=1
    )

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

def get_pie(glc):
    hypo2 = (glc<3).sum()
    hypo1 = ((glc>=3) & (glc<3.9)).sum()
    norm = ((glc>=3.9 )& (glc<=10)).sum()
    hyper1 = ((glc>10) & (glc<=13.9)).sum()
    hyper2 = (glc>13.9).sum()
    return [hypo2, hypo1, norm, hyper1, hyper2]
    

def create_pie_chart(df):
    values = get_pie(df.glc)
    labels = ['Level 2 hypoglycemia (<3mmol/L)', 'Level 1 hypoglycemia (3-3.9mmol/L)', 'Normal range (3.9-10mmol/L)', 'Level 1 hyperglycemia (10-13.9mmol/L)','Level 2 hyperglycemia (>13.9mmol/L)',]
    
    fig = go.Figure()
    fig.add_trace(go.Pie(values=values, labels=labels, marker_colors=colors, opacity=0.5),)
    fig.update_layout(
        title = 'Percentage time in range')
        
    return html.Div([
            dcc.Graph(
                        id='pie-chart',
                        figure=fig
            )
    ])

def create_amb_glc_profile(df):
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
    #fig.update_xaxes(showgrid=False, zeroline=False)
    #fig.update_yaxes(showgrid=False, zeroline=False)
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
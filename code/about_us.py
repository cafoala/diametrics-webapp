import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_player as dp

about_us_layout = html.Div([
    html.H1('About Us'),
    html.P(''),
    dbc.Card(
    [dbc.CardHeader(html.H3('The Team'),),
    dbc.CardBody(dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H4('Cat Russon'),
            html.Img(src='assets/Cat_Russon.jpg', width='180px'),
            html.P('Cat\'s a PhD student with a good heart and bad habits')
        ]), color='light')),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H4('Rob Andrews'),
            html.Img(src='assets/Rob_Andrews.jpg', width='180px'),
            html.P('Rob is a consultant diabetologist and the clinical advisor for this project')
        ]), color='light')),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H4('Michael Saunby'),
            html.Img(src='assets/michael-saunby.jpeg', width='180px'),
            html.P('Technical advisor')
        ]), color='light')),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H4('Mike Allen'),
            html.Img(src='assets/Mike-Allen.jpg', width='180px'),
            html.P('Data science wizz')
        ]), color='light')),
    ]))])
])
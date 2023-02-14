import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Welcome to Diametrics", className="display-3"),
            html.P(
                "A no-code webtool for calculating the metrics of glycemic control and exploring continuous glucose monitoring (CGM) data",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "Use utility classes for typography and spacing to suit the "
                "larger container."
            ),
            html.P(
                dbc.Button("Learn more", color="primary"), className="lead"
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
)


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "16rem",
    "margin-right": "2rem",
    "padding": "1.5rem 1rem",
}

sidebar = html.Div(
    [
        html.H3("Diametrics", className="display-6"),
        html.Hr(),
        html.P("Calculate the metrics of glycemic control",
            className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Dashboard", href="/page-1", active="exact"),
                dbc.NavLink("Instructions", href="/page-2", active="exact"),
                dbc.NavLink("About Us", href="/page-3", active="exact"),
                dbc.NavLink("Contact", href="/contact", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    className="h-100 p-4 text-white bg-dark",
)

content = html.Div([
    jumbotron], style=CONTENT_STYLE)

def create_home_layout():
    return html.Div([dcc.Location(id="url"), sidebar, content])
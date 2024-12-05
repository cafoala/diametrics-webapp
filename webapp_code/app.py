from dash import Dash, html, dcc, callback, Input, Output
import dash
import os
import dash_bootstrap_components as dbc
import layout
import about_us
import contact
import dash_uploader as du
import ssl
import smtplib

external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = Dash(__name__, external_stylesheets = external_stylesheets, use_pages=True)
app.config.suppress_callback_exceptions = True

app.title = 'Diametrics'
app._favicon = (os.path.join('assets', 'favicon.ico'))


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30vh",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "45vh",
    "margin-right": "2rem",
    "padding": "1.5rem 1rem",
}

sidebar = html.Div(
    [
        html.Br(),
        html.Img(src='assets/logo_circle.png', width='180px'),  
        html.Br(),
        html.H3("Diametrics", className="display-6"),
        html.Hr(),
        html.P("Advanced CGM Data Analysis Made Easy",
            className="lead"
        ),
        html.Br(),
        dbc.Nav(
            [
                dbc.NavLink(html.H6([html.I(className="bi bi-house"),"  Home"]), href="/", active="exact"),
                dbc.NavLink(html.H6([html.I(className="bi bi-speedometer"), "  Dashboard"]), href="/dashboard", active="exact"),
                dbc.NavLink(html.H6([html.I(className="bi bi-book"), "  Documentation"]), href="/documentation", active="exact", target="_blank"),
                dbc.NavLink(html.H6([html.I(className="bi bi-file-earmark-person"), "  About Us"]), href="/about", active="exact"),
                dbc.NavLink(html.H6([html.I(className="bi bi-envelope"), "  Contact"]), href="/contact", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    className="h-100 p-4 text-white bg-dark",)

content = html.Div(id='content', style=CONTENT_STYLE)
app.layout = html.Div([
	dcc.Location(id="url"), sidebar, content
    ])

@callback(Output('content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
         return layout.jumbotron
    elif pathname == '/dashboard':
         return layout.content
    elif pathname == '/documentation':
        return layout.instruction_section
    elif pathname == '/about':
        return about_us.about_us_layout
    elif pathname == '/contact':
        return contact.contact_form()
    else:
        return '404'


if __name__ == '__main__':
    # DASH_PORT is set to 80 in Dockerfile
    port = os.environ.get('DASH_PORT', 8050)
    app.run_server(debug=False, host='0.0.0.0', port=port) #, dev_tools_ui=False)
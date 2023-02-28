from dash import Dash, html, dcc, callback, Input, Output
import dash
import os
import dash_bootstrap_components as dbc
import layout
import dash_uploader as du
image_path = 'assets/logo_circle.png'

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
    "width": "25vh",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "30vh",
    "margin-right": "2rem",
    "padding": "1.5rem 1rem",
}

sidebar = html.Div(
    [
        html.Img(src=image_path, width='180px'),  
        html.H3("Diametrics", className="display-6"),
        html.Hr(),
        html.P("Calculate the metrics of glycemic control",
            className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
                dbc.NavLink("Instructions", href="/instructions", active="exact"),
                dbc.NavLink("About Us", href="/page-3", active="exact"),
                dbc.NavLink("Contact", href="/contact", active="exact"),
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
    elif pathname == '/instructions':
        return layout.instruction_section

    else:
        return '404'

if __name__ == '__main__':
    # DASH_PORT is set to 80 in Dockerfile
    port = os.environ.get('DASH_PORT', 8050)
    app.run_server(debug=True, host='0.0.0.0', port=port) #, dev_tools_ui=False)
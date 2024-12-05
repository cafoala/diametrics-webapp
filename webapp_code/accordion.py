import dash_bootstrap_components as dbc
from dash import Input, Output, html
import dash

external_stylesheets = [dbc.themes.JOURNAL]
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#, suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True

accordion = html.Div(
    [
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    dbc.Button('press me', id='button'),
                    title="Item 1",
                    item_id="item-1",
                ),
                dbc.AccordionItem(
                    "This is the content of the second section",
                    title="Item 2",
                    item_id="item-2",
                ),
                dbc.AccordionItem(
                    "This is the content of the third section",
                    title="Item 3",
                    item_id="item-3",
                ),
            ],
            id="accordion",
            active_item="item-1",
        ),
        dbc.Accordion(
        html.Div(id='more-accordions'),
        ),
        html.Div(id="accordion-contents", className="mt-3"),
    ]
)

app.layout = html.Div([
    accordion
])

@app.callback(
    Output("more-accordions", "children"),
    [Input("button", "n_clicks")],
)
def return_accordions(n_clicks):
    if n_clicks is not None:
        return dbc.AccordionItem(
                        "This is the content of the second section",
                        title="Item +",
                        item_id="item-4",
                    ),

@app.callback(
    Output("accordion-contents", "children"),
    [Input("accordion", "active_item")],
)
def change_item(item):
    return f"Item selected: {item}"
if __name__ == '__main__':
    app.run_server(debug=True)#, dev_tools_ui=False)

### Run with pytest don't ask why
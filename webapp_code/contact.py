import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_player as dp

contact_info = html.Div([
                    html.P("Contact Information", style={"font-size": "24px"}),
                    dcc.Markdown('''Project Email: [diametrics@proton.me](mailto:diametrics@proton.me)''', style={"font-size": "16px"}),
                    dcc.Markdown('''Cat's Email: [cr91@exeter.ac.uk](mailto:cr591@exeter.ac.uk)'''),#, style={"font-size": "16px"}),
                    dcc.Markdown('''Cat's LinkedIn: [https://uk.linkedin.com/in/catherine-russon](https://uk.linkedin.com/in/catherine-russon)''')
                ], style={
                    "border": "2px solid #ccc",
                    "border-radius": "5px",
                    "padding": "10px",
                    "margin": "10px",
                })

def contact_form():
    markdown = '''
    We welcome any feedback you have about Diametrics. This is a small project and any problems you find can help us to make the tool better!
      

    Send us an email if you have any comments, questions, or would like to be involved in the project. 
    
  
    Thank you!
    
    '''   
    form = html.Div([ 
        html.H1('Contact'),
        dbc.Card(dbc.CardBody([
            
            dcc.Markdown(markdown),
            contact_info,
        ]))
        ])
    
    return form
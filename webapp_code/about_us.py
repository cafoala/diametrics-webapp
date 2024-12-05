import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_player as dp

about_us_layout = html.Div([
    html.H1('About Us'),
    html.P(''),
    
    dbc.Card(
    [dbc.CardHeader(html.H3('Reference'),),
    dbc.CardBody([

        dcc.Markdown(
            '''
            If you use Diametrics in your research, please reference us! :D
 
            Russon, Catherine L., et al. "A User-Friendly Web Tool for Custom Analysis of Continuous Glucose Monitoring Data." Journal of Diabetes Science and Technology 18.6 (2024): 1511-1513 - it's available [here](https://journals.sagepub.com/doi/full/10.1177/19322968241274322?casa_token=9uruVbvGbZYAAAAA%3AceTcASVJ-jzQFWbmO-XnKBWv11AZ4FK450RLdzHdHtuPDqTkn9tK8wSFFOp0c9xaPRSZwOtzmrI).
    ''')])]),


    dbc.Card(
    [dbc.CardHeader(html.H3('The Project'),),
    dbc.CardBody([

        dcc.Markdown(
            '''
            The aim of this project was to make a simple, flexible tool to calculate the metrics of glycemic control from continuous glucose monitoring (CGM) data.

            Continuous glucose monitors are an exciting new development in the management of type 1 diabetes (T1D). These devices give glucose readings every 5 to 15 minutes, providing large amounts of data and providing potential for unprecedented insight into glucose dynamics throughout the day.
            NICE has recently announced that all people with type 1 diabetes will receive a CGM. This dramatic increase in data will provide opportunity for significant advances in diabetes health research, but will naturally result in an increased demand for effective data analysis tools for non-technical researchers and clinicians.

            The [international consensus on the use of continuous glucose monitors](https://diabetesjournals.org/care/article/40/12/1631/37000/International-Consensus-on-Use-of-Continuous) (CGMs) has identified several metrics of glycemic control that are important for assessing and optimizing diabetes management.
            However, the current platforms on which CGM data analysis can be performed are proprietary, closed source and limited in terms of functionality. The glucose data can be analysed with some basic metrics but cannot be explored in any more flexible or complex ways. Consequently, researchers are exporting the data and calculating the relevant metrics manually, which is extremely time consuming and prone to error.

            The idea of this project began when Cat was approached to try to solve this problem... and thus, Diametrics was born. The WebApp allows researchers to easily calculate the metrics of glycemic control whilst also providing an unprecendented freedom to explore the data further.
            Diametrics can be used to calculate the commonly used metrics of glycaemic control, explore your data through interactive visualisations and break your data down into specific periods of interest.
    ''')])]),

    dbc.Card(
        [dbc.CardHeader(html.H3('The Team'),),
        dbc.CardBody(dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                dcc.Link(html.H4('Cat Russon'), 'https://medicine.exeter.ac.uk/people/profile/index.php?web_id=Cat_Russon'),
                html.Img(src='assets/Cat_Russon.jpg', width='180px'),
                html.P('Health data science PhD student and project lead')
            ]), color='light')),
            dbc.Col(dbc.Card(dbc.CardBody([
                dcc.Link(html.H4('Rob Andrews'), 'https://medicine.exeter.ac.uk/people/profile/index.php?web_id=Rob_Andrews'),
                html.Img(src='assets/Rob_Andrews.jpg', width='180px'),
                html.P('Consultant diabetologist and the clinical advisor')
            ]), color='light')),
            dbc.Col(dbc.Card(dbc.CardBody([
                dcc.Link(html.H4('Michael Saunby'), 'https://computerscience.exeter.ac.uk/staff/ms843?sm=ms843'),
                html.Img(src='assets/michael-saunby.jpeg', width='180px'),
                html.P('Software engineer and technical advisor')
            ]), color='light')),
            dbc.Col(dbc.Card(dbc.CardBody([
                dcc.Link(html.H4('Mike Allen'), 'https://arc-swp.nihr.ac.uk/about-penarc/people/mike-allen/'),
                html.Img(src='assets/Mike-Allen.jpg', width='180px'),
                html.P('Health data scientist and technical advisor')
            ]), color='light')),
        ]))]),

    dbc.Card([
            dbc.CardHeader(html.H3('Acknowledgments')),
            dbc.CardBody([
                dbc.Row(
                    dcc.Markdown(
                        '''
                        All of the team are affiliated with the [University of Exeter](https://www.exeter.ac.uk/), where Cat is doing her PhD under the supervision of Rob Andrews, Mike Allen, Richard Pulsford and Neil Vaughan. 
                        
                        This project was selected and funded by Emily Paremain at [The Alan Turing Institute](https://www.turing.ac.uk/) at University of Exeter. 
                        
                        The University of Exeter [Research Software Engineering](https://www.exeter.ac.uk/research/idsai/team/researchsoftwareengineers/) team, led by Katie Finch, provided technical support and guidance. 
                        
                        A massive thank you to the participants of the [Exercise in Type 1 Diabetes (EXTOD)](https://extod.org/) and [Motivate](https://www.motivateljmu.com/) trials, whose data we wouldn\'t have been able to build this WebApp!
                        
                        Finally, thank you to Katie Hesketh, Jonathon Low, Matt Cocks, Nick Jones, and Joséphine Molveau for your feedback and support <3''')
                ),
                dbc.Row([

                dbc.Col(dbc.Card(dbc.CardBody(
                    html.Img(src='assets/exeter_logo.svg', width='180px')), color='secondary')),
                                
                dbc.Col(dbc.Card(dbc.CardBody(html.Img(src='assets/turing_logo.svg', width='180px')), color='secondary')),

                dbc.Col(dbc.Card(dbc.CardBody(html.Img(src='assets/motivate_logo.webp', width='180px')), color='secondary')),
                
                dbc.Col(dbc.Card(dbc.CardBody(html.Img(src='assets/extod_logo.svg', width='180px')), color='secondary')),
                ])
            ])])
])
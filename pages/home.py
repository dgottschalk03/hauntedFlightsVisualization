'''
Home page
Rendered by calls to dbc components
'''
from dash import register_page, html, dcc
import dash_bootstrap_components as dbc

register_page(__name__, path='/', title='Haunted Flights Explorer') # https://dash.plotly.com/urls

with open('static/home.md', 'r') as f:
    body = f.read()

layout = [
        dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H1('Haunted Flights Explorer'),
                className="text-center mt-3 mb-3"  
                )    
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Markdown(
                                body,
                                dangerously_allow_html=True,
                                mathjax=True,
                                className="fs-5",
                            )
                        )
                    )

                )
            ),

            dbc.Row(
                dbc.Col(
                    dbc.Stack(
                        [
                            dbc.Button(
                                [
                                    html.I(className="fab fa-github me-2"),
                                    'Code on Github'
                                ], 
                                href="https://github.com/dgottschalk03/hauntedFlightsVisualization",
                                target="_blank", 
                                color="primary",
                                className = "me-2 w-auto"),
                            dbc.Button(
                                'Interactive Map', 
                                href="/flight-explorer",
                                target="_blank", 
                                color="primary",
                                className = "me-2 w-auto"),                                
                        ],
                        gap = 3,
                        className = "mb-3",
                        direction = "horizontal"
                    ),
                width = "auto",
                className = "mt-3 mx-auto"
                ),
            ),

            dbc.Row(
                dbc.Col(
                    html.H2(
                        "✈️ Happy Flying! ✈️",
                        className="text-center my-4",
                    ),
                    width=12,
                )
            ),

            dbc.Row(
                dbc.Col(
                    html.Img(
                        src="/static/map_sample.png",
                        width="100%",
                        className = "mx-0 mb-3 rounded"
                    )
                )
            ),

            
        ],
    fluid = "lg",
    )
]


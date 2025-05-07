from dash import register_page, dcc, html
import dash_bootstrap_components as dbc

register_page(module=__name__,
              name="Sources",
              title="Sources")

with open('static/sources.md', 'r') as f:
    body = f.read()

layout = [
        dbc.Container(
        [

            dbc.Row(
                dbc.Col(
                    html.H1('Haunted Flights Explorer'),
                className="text-center"  
                )    
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Markdown(
                                body,
                                mathjax=True,
                                className="fs-5",
                            )
                        )
                    )

                )
            ),
        ],
    fluid = "lg",
    )
]


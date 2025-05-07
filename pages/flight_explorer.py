# -- From https://dash.plotly.com/tutorial
from dash import html, dash_table, dcc, callback, Output, Input, register_page, ctx
import dash_bootstrap_components as dbc

# Helper Functions #
from utils.dataLoader import load_all_data
from core import callback_sidebar
from defaultlayouts import leftsidebar

register_page(module=__name__,
              name="Interactive Map",
              title='Interactive Map')

# Load data
hp_df, route_df, airport_df = load_all_data()

# Register callbacks
callback_sidebar.register_map_callbacks(hp_df, route_df, airport_df)

# App layout
layout = [
    html.Div(
        children = leftsidebar.side_navbar(hp_df = hp_df),
        className = "page-navbar",
        id = 'sidebar-container'
    ),
    dbc.Button(
                ">",
                id="toggle-sidebar-btn",
                color="primary",
                size = "sm",
                className="sidebar-toggle-btn me-2",  
                n_clicks=0
            ),
    dbc.Container(
        [ 
        html.H2(
            "Haunted Flights Explorer",
            className = "text-center fs-3",
            style = {"fontWeight": "bold"}
        ),
        dcc.Loading(
            id="loading-interactive-map",
            type="default",  
            color="#F27405",  
            children=[
                dcc.Graph(id='interactive-map',
                style={'height': '90vh', 'width': '100%', 'margin': 'auto'}
                )
            ]
        )
    ],
    fluid = True)
]

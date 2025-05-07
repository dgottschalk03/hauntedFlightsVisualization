from dash import html, dcc, page_registry
from dash import callback, Output, Input, ctx
import dash_bootstrap_components as dbc
from core.mapbuttons import mapDropdown, holidayDropdown, dateInput, coloringDropdown, sizeDropdown, airportDropdown, airportVisibilityDropdown
from core import callback_sidebar
import pandas as pd

def side_nav_content(idprefix:str="", hp_df : pd.DataFrame = None):
    """
    Common content for both versions of side navbar
    idprefix, different between bar and drawer, must be used for all ids to avoid duplication errors
    """
    nav_data = page_registry.values()
    nav_content = [
            html.H5("Fright Filters", className="mt-3 mb-3", style={'textAlign': 'center'}),
            dbc.Stack(
                [
                mapDropdown('State', hp_df = hp_df),
                mapDropdown('Event_Type', hp_df = hp_df, init_value = ["Plane_Crash", "Flying_Object"]),
                mapDropdown('Apparition_Type', hp_df = hp_df),
                holidayDropdown(),
                coloringDropdown(),
                sizeDropdown(),
                dateInput(),
                ],
                gap = 3,
            )] + \
            [
            html.H5("Flight Filters", className="mt-3 mb-3", style={'textAlign': 'center'}),
            dbc.Stack(
                [
                airportDropdown(),
                dbc.Label("Toggle Visibility", style = {'textAlign': 'center', "color": "#F5B234"}),
                airportVisibilityDropdown()
                ],
                gap = 3, 
            ),
            ] + \
            [html.Div(
                dbc.Button("Apply Filters", color="primary", id=f"{idprefix}-apply-btn", className="mx-auto mb-3"),
                className = "d-flex justify-content-center mt-3")
            ]
    return nav_content

# --------------------------------------------
def side_navbar_link(nav_entry):
    link = html.Li( 
            dcc.Link(nav_entry["name"], href=nav_entry["path"]),
        )
    return link
# --------------------------------------------
def side_navbar(hp_df : pd.DataFrame = None):
    contents = [
            html.H3("Map Settings", style = {'textAlign': 'center'}),
            html.P("Toggle your desired spooky settings and press apply.", style = {'textAlign': 'center'}),
    ] + side_nav_content(idprefix="bar", hp_df = hp_df)
    return contents
# --------------------------------------------
def navbar_drawer(hp_df : pd.DataFrame = None):
    contents = [
            html.P("Uses dbc.Offcanvas"),
            html.P("This drawer becomes available when screen width is below 1200px"),
    ] + side_nav_content(idprefix="drawer", hp_df = hp_df)
    return contents
# --------------------------------------------
def popup_title():
    return "Left side popup"
# --------------------------------------------

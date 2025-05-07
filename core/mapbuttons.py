from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.query import get_legend_items
import pandas as pd


def mapDropdown(id: str = "", hp_df : pd.DataFrame = None, init_value =  []):

    return  dcc.Dropdown(
            id={'type': 'attribute-filter-dropdown', 'subtype': id}, 
            options=[{'label': s.replace('_', ' '), 'value': s} for s in sorted(get_legend_items(hp_df, id))],
            multi=True,
            value = init_value,
            placeholder=f"{id.replace('_', ' ')}",
            className="bootstrap-dropdown",
        )

def dateInput():
    return html.Div(
        [
            # Date Start
            html.Div(
                [
                    html.Label("Start Date", className="text-center mb-1"),
                    dbc.Row(
                        [
                            dbc.Col(dbc.Input(type="number", min=1600, max=2026, step=10, value=1950, id="start-year"), width=4),
                            dbc.Col(dbc.Input(type="number", min=1, max=12, step=1, value=1, id="start-month"), width=3),
                            dbc.Col(dbc.Input(type="number", min=1, max=31, step=1, value=1, id="start-day"), width=3),
                            dbc.Col(
                                dbc.Checklist(options = [{"label": "", "value": ""}],id="include-start-date", value = [], switch = True, inline = True), 
                                width = "auto", 
                                style={"display": "flex", "alignItems": "center", "justifyContent": "center"}
                                )
 
                        ],
                        className="g-2",
                    ),
                ],
                className="text-center mb-3",
            ),

            # Date End
            html.Div(
                [
                    html.Label("End Date", className="text-center mb-1"),
                    dbc.Row(
                        [
                            dbc.Col(dbc.Input(type="number", min=1600, max=2026, step=10, value=2020, id="end-year"), width=4),
                            dbc.Col(dbc.Input(type="number", min=1, max=12, step=1, value=1, id="end-month"), width=3),
                            dbc.Col(dbc.Input(type="number", min=1, max=31, step=1, value=1, id="end-day"), width=3),
                            dbc.Col(
                                dbc.Checklist(options = [{"label": "", "value": ""}], id="include-end-date", value = [], switch = True, inline = True), 
                                width = "auto", 
                                style={"display": "flex", "alignItems": "center", "justifyContent": "center"}
                                )

                        ],
                        className="g-2",
                    ),
                ],
                className="text-center mb-3",
            )
        ]
    )
def holidayDropdown():
    holidays = [
    {"label": "All Holidays", "value": "all"},
    {"label": "New Year's Day", "value": "1000-1-1"},
    {"label": "Valentine's Day", "value": "1000-2-14"}, 
    {"label": "St. Patrick's Day", "value": "1000-3-17"},
    {"label": "April Fool's", "value": "1000-4-1"}, 
    {"label": "Easter", "value": "1000-4-20"},
    {"label": "Independence Day", "value": "1000-7-4"},
    {"label": "Halloween", "value": "1000-10-31"},
    {"label": "Thanksgiving", "value": "1000-11-23"},
    {"label": "Christmas Eve", "value": "1000-12-24"},
    {"label": "Christmas Day", "value": "1000-12-25"},
]
    return  dcc.Dropdown(
            id=({"type": "attribute-filter-dropdown", "subtype": "holiday-dropdown"}),
            options=holidays,                
            multi=True,
            placeholder="Select Holiday", 
            className="bootstrap-dropdown",
    )

def coloringDropdown():
    return  dcc.Dropdown(
            id='coloring-toggle',
            options=[
                {'label': 'Event Type', 'value': 'Event_Type'},
                {'label': 'Apparition Type', 'value': 'Apparition_Type'},
                {'label': 'Time of Day', 'value': 'Time_of_Day'},
                {'label': 'Audio Evidence', 'value': 'Audio_Evidence'},
                {'label': 'Visual Evidence', 'value': 'Visual_Evidence'},
                {'label': 'High Traffic Flight', 'value': 'Flight_HighTraffic'},
                {'label': 'Airport Proximity', 'value': 'Aerodrome_Proximity'}
            ],
            value='Event_Type',
            placeholder = 'Color Locations By: ',
            className="bootstrap-dropdown",
            clearable=True,
            multi = False
        )

def sizeDropdown():
    return dcc.Dropdown(
        id = 'size-arg',
        options = [
            {"label": "Flight Intersection Count", "value": "Flight_Intersection_Count"},
            {"label": "Witness Count", "value": "Haunted_Places_Witness_Count"},
            {"label": "Nearby Airports", "value": "Aerodrome_Count"}
        ],
        value = "Flight_Intersection_Count",
        placeholder = 'Size Locations By: ',
        className = "bootstrap-dropdown",
        clearable = True,
        multi = False

    )
def airportDropdown():
    airports = [
    {"label": "Large Airport", "value": "large_airport"},
    {"label": "Medium Airport", "value": "medium_airport"},
    {"label": "Small Airport", "value": "small_airport"}, 
    {"label": "Heliport", "value": "heliport"},
    {"label": "Seaplane Base", "value": "seaplane_base"}, 
    {"label": "Balloonport", "value": "balloonport"},
    {"label": "Toggle All", "value": 'all'},
    ]

    return  dbc.Checklist(
            id='airport-type-checklist',
            options=airports,
            value = ['large_airport', 'medium_airport'],
            switch = True,
            style={
                'display': 'flex', 
                'flexDirection': 'column', 
                'justifyContent': 'center', 

            }
        )

def airportVisibilityDropdown():

    return  dbc.Checklist(
            id='airport-visibility-checklist',
            options=[{"label": "Airports", "value": "airports"}, {"label": "Routes", "value": "routes"}],
            value = ['airports', 'routes'],
            switch = True,
            style={
                'display': 'flex', 
                'flexDirection': 'row', 
                'justifyContent': 'center', 
                'gap': '2rem'
            }
        )

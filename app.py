## Imports ##
# Plotly #
import plotly.graph_objects as go
import plotly.express as px

# Dash #
import dash
from dash import dcc, html, Input, Output, ctx

# Helper Functions #
from plots.interactiveMap import hp_interactive_darkmatter
from utils.query import filter_airport_df, filter_hp_df, filter_route_df, get_legend_items, transform_year
from utils.dataLoader import load_all_data

## Load Data and Define Holidays
hp_df, route_df, airport_df = load_all_data()

holidays = [
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

airports = [
    {"label": "Toggle All", "value": 'all'},
    {"label": "Heliport", "value": "heliport"},
    {"label": "Seaplane Base", "value": "seaplane_base"}, 
    {"label": "Balloonport", "value": "balloonport"},
    {"label": "Small Airport", "value": "small_airport"}, 
    {"label": "Medium Airport", "value": "medium_airport"},
    {"label": "Large Airport", "value": "large_airport"},
]

## Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([

    # Title
    html.H1("Haunted Flights Explorer"),

    # Section 1: Haunted paces filtering
    html.Div([

    html.H2("Haunted Places Filters", style={'marginTop': '20px', 'marginBottom': '10px'}),
    
    html.Div(style={'height': '10px'}),  

        html.Div([
            html.Div([
                #html.Label("State:"),
                dcc.Dropdown(
                    id='State',
                    options=[{'label': s.replace('_', ' '), 'value': s} for s in sorted(get_legend_items(hp_df, 'State'))],
                    multi=True,
                    placeholder="Select a State"
                ),
            ], style={'height': '10px','width': '12.5%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '1%'}),

            html.Div([
                #html.Label("Event Type:"),
                dcc.Dropdown(
                    id='Event_Type',
                    options=[{'label': s.replace('_', ' '), 'value': s} for s in sorted(get_legend_items(hp_df, 'Event_Type'))],
                    multi=True,
                    placeholder="Select Event Type"
                ),
            ], style={'width': '12.5%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '1%'}),

            html.Div([
                #html.Label("Apparition Type:"),
                dcc.Dropdown(
                    id='Apparition_Type',
                    options=[{'label': s.replace('_', ' '), 'value': s} for s in sorted(get_legend_items(hp_df, 'Apparition_Type'))],
                    multi=True,
                    placeholder="Select Apparition Type"
                ),
            ], style={'width': '12.5%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '1%'}),
            
            html.Div([
                #html.Label("Holiday:"),
                dcc.Dropdown(
                    id='holiday-dropdown',
                    options=holidays,                
                    multi=True,
                    placeholder="Select Holiday"
                ),
            ], style={'width': '12.5%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '1%'}),
            
            html.Div([
                #html.Label("Color Locations by:"),
                dcc.Dropdown(
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
                    clearable=True,
                ),
            ], style={'width': '12.5%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        ], style={'whiteSpace': 'nowrap'}),

    # Subsection 1.1: Year Slider

    html.Div(style={'height': '10px'}),  

        html.Div([

            html.Div([
                html.Label("Year Range:"),
                dcc.RangeSlider(
                    min = 1780, 
                    max = 2025,
                    id='year-slider',
                    marks={
                        1780 : '1600',
                        1785 : '1650',
                        1790 : '1700',
                        1795 : '1750', 
                        **{1800 + 20 * i: '{}'.format(1800 + 20 * i) for i in range(10)},
                        **{1900 + 20 * i: '{}'.format(1900 + 20 * i) for i in range(10)},
                        2000: '2000',
                        2020: '2020',
                    },
                    value=[1900, 1950],
                    dots=False,
                    step=1,
                    updatemode='drag',
                    allowCross = False,
                    tooltip={
                        "placement": "bottom",
                    },
                ),
            ], style={'width': '90%', 'display': 'inline-block', 'paddingLeft': '0px', 'verticalAlign': 'top'}),

            html.Div([
                dcc.Checklist(
                    id='apply-year-toggle',
                    options=[{'label': 'Apply', 'value': 'on'}],
                    value=[],  
                    style={'marginTop': '10px'}
                ),
            ], style={'width': '5%', 'display': 'inline-block', 'paddingLeft': '5px', 'verticalAlign': 'top'}),

        ], style={'whiteSpace': 'nowrap'}), 
    ]),
    
    html.Br(), 

    # Section 2 - Flight Options
    html.Div([
        html.H2("Flight Fliters", style={'marginTop': '20px', 'marginBottom': '10px'}),
        
        html.Div(style={'height': '10px'}),  

        html.Div([

            html.Div([
                html.Label("Airport Type:"),
                dcc.Checklist(
                    id='airport-type-checklist',
                    options=airports,
                    value = [],
                    inputStyle={"margin-right": "5px", "margin-left": "10px"},
                    style={'display': 'flex', 'flexDirection': 'row'}
                ),
            ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '1%'}),
            
            html.Div([
                html.Label("Toggle Visibility:"),
                dcc.Checklist(
                    id='airport-visibility-checklist',
                    options=[{"label": "Airports", "value": "airports"}, {"label": "Routes", "value": "routes"}],
                    value = [],
                    inputStyle={"margin-right": "5px", "margin-left": "10px"},
                    style={'display': 'flex', 'flexDirection': 'row'}
                ),
            ], style={'width': '24%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '1%'}),

        ], style={'whiteSpace': 'nowrap'}),
    ]),

    #dcc.Graph(id='geo-plot')
    dcc.Loading(
    id="loading-geo-plot",
    type="default",  # or "circle", "dot", "cube", etc.
    color="#F27405",  # optional: set color (green example)
    children=[
        dcc.Graph(id='geo-plot',
        style={'height': '90vh', 'width': '95vw', 'margin': 'auto'})
    ],
    #style={'height': '800px', 'width': '100%'},
)
])



@app.callback(
    Output('geo-plot', 'figure'),
    Input('State', 'value'),
    Input('Event_Type', 'value'),
    Input('Apparition_Type', 'value'),
    Input('year-slider', 'value'),
    Input('apply-year-toggle', 'value'),
    Input('holiday-dropdown', 'value'),
    Input('coloring-toggle', 'value'),
    Input('airport-type-checklist', 'value'),
    Input('airport-visibility-checklist', 'value')
)
def update_figure(state, event_type, apparition_type, year_range, year_toggle, holiday, coloring_toggle, airport_types, airport_visibility):
    
    # extract triggered arguments from callback
    triggered_inputs = {k.split('.')[0]: v for k, v in ctx.inputs.items()}
    # additional arguments displayed on hover
    additional_tags = [arg for arg, v in triggered_inputs.items() if arg not in  ['coloring-toggle', 'airport-type-checklist', 'airport-visibility-checklist'] and v is not None]
    # Transform year range for query
    if year_toggle:
        year_range = [f"{transform_year(year)}-01-01" for year in year_range]
    else:
        year_range = None
    # define coloring
    coloring = {coloring_toggle: get_legend_items(hp_df, coloring_toggle)}



    # Filter Data
    filtered_hp_df = filter_hp_df(hp_df, state, event_type, apparition_type, year_range, holiday)
    filtered_route_df = filter_route_df(filtered_hp_df, route_df)
    filtered_airport_df = filter_airport_df(filtered_hp_df, airport_df, airport_types)
    filtered_hp_df = filtered_hp_df.astype(str)

    return hp_interactive_darkmatter(filtered_hp_df, filtered_route_df, filtered_airport_df, coloring, additional_tags, airport_visibility)



if __name__ == '__main__':
    app.run(debug=True)
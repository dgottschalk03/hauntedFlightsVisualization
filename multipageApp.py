import dash 
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from utils.dataLoader import load_all_data
from pages.p2_map import get_layout as map_layout
from pages.p2_map import register_callbacks
from pages.p1_overview import get_overview_layout
from pages.p3_source import get_source_layout


app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.MINTY])

app.title = "Haunted Flights Explorer"

# Load Data and Define Holidays
hp_df, route_df, airport_df = load_all_data()

# Load map layout and data
map_page = map_layout(hp_df)

navbar = dbc.NavbarSimple(
    brand="Haunted Flights Explorer",
    brand_href="#",
    color="primary",
    dark=True,
    children=[
        dbc.NavItem(dbc.NavLink("Overview", href="#", id="nav-overview")),
        dbc.NavItem(dbc.NavLink("Explorer", href="#", id="nav-explorer")),
        dbc.NavItem(dbc.NavLink("Sources", href="#", id="nav-sources")),
    ],
    className="mb-4",
)

app.layout = dbc.Container(
    [
        
        html.H1("Haunted Flights Explorer", className="my-title text-center mb-4"),
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='Overview', value='tab-1', className='custom-tab', selected_className='tab--selected'),
            dcc.Tab(label='Interactive Map', value='tab-2', className='custom-tab', selected_className='tab--selected'),
            dcc.Tab(label='Sources', value='tab-3', className='custom-tab', selected_className='tab--selected'),
        ]),
        # navbar,
        html.Div(id='tabs-content', className="mt-4")
    ],
    fluid=True,  # Or False if you want it boxed
)

register_callbacks(app, hp_df, route_df, airport_df)

@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return get_overview_layout()
    elif tab == 'tab-2':
        return map_page
    elif tab == 'tab-3':
        return get_source_layout()

if __name__ == '__main__':
    app.run(debug=True)
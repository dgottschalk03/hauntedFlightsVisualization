import dash
from dash import Input, Output, State, callback, ctx
from dash.dependencies import MATCH
import json

from plots.interactiveMap import hp_interactive_darkmatter
from utils.query import filter_airport_df, filter_hp_df, filter_route_df, get_legend_items

def extract_additional_tags(state_dict, target_type="attribute-filter-dropdown"):
    """
    Extracts 'subtype' values from pattern-matching keys in a Dash state or input dictionary.

    Args:
        state_dict (dict): Typically ctx.states or ctx.inputs.
        target_type (str): The 'type' to match (default: 'attribute-filter-dropdown').

    Returns:
        List[str]: A list of subtype values.
    """
    excluded_keys = ['start-year', 'start-month', 'start-day', 'end-year', 'end-month', 'end-day','coloring-toggle', 'airport-type-checklist', 'airport-visibility-checklist', 'holiday-dropdown']
    res = {}

    for k, v in state_dict.items():
        key_part = k.split('.')[0]  
        try:
            parsed = json.loads(key_part)
            if (
                isinstance(parsed, dict)
                and parsed.get('type') == target_type
                and 'subtype' in parsed
                and v not in (None, [])
            ):
                res[parsed['subtype']] = v
        except json.JSONDecodeError:
            continue  # Skip non-JSON keys
    res = {s: v for s, v in res.items() if s not in excluded_keys}
    return res

# Sidebar Hider Callback
@callback(
    Output("sidebar-container", "className"), # Side bar state
    Output("page-body", "className"),         # Page Body state
    Output("toggle-sidebar-btn", "children"),  # Button text
    Input("toggle-sidebar-btn", "n_clicks"),
    State("sidebar-container", "className"),
    State("page-body", "className"), 
    prevent_initial_call=True
) 
def toggle_sidebar(n_clicks, sidebar_class, body_class):
    '''
    Hides side panel and expands body of page to fit when ">" button is clicked. 
    '''
    if "hidden" in sidebar_class:
        # Sidebar is currently hidden → we want to **show** it now
        new_sidebar_class = sidebar_class.replace(" hidden", "") # remove hidden from sidebar class
        new_body_class = body_class.replace(" body-expanded", "") # shrink page body to fit
        button_text = "<"  
    
    else:
        new_sidebar_class = sidebar_class + " hidden" # hide sidebar
        if "body-expanded" not in body_class:
            new_body_class = body_class + " body-expanded" # expand page body to fit
        else:
            new_body_class = body_class
        button_text = ">" 

    return (new_sidebar_class, new_body_class, button_text)

# Custom "Toggle All" Callback for attribute dropdowns
@callback(
    Output({'type': 'attribute-filter-dropdown', 'subtype': MATCH}, 'value'),
    Input({'type': 'attribute-filter-dropdown', 'subtype': MATCH}, 'value'),
    prevent_initial_call=True
)

def enforce_all_exclusivity(selected):
    ''' 
    If "toggle all" is selected, keep only "toggle all"
    '''
    if not selected:
        return dash.no_update
    
    # If All is selected along with other values, keep only All
    if "all" in selected and len(selected) > 1:
        return ["all"]
    return dash.no_update

# Custom Airport Type "Toggle All" Callback
airport_types = ["heliport", "seaplane_base", "balloonport", "small_airport", "medium_airport", "large_airport"]

@callback(
    Output('airport-type-checklist', 'value'),
    Input('airport-type-checklist', 'value'),
    State('airport-type-checklist', 'value'),
    prevent_initial_call=True
)
def toggle_airports(selected_values, previous_values):
    triggered = ctx.triggered_id

    if 'all' in selected_values:
        # Check if all are already selected → deselect
        if all(atype in previous_values for atype in airport_types):
            return []
        else:
            return airport_types
    else:
        return selected_values

# Update Map Callback
hp_df = None  
route_df = None
airport_df = None 

def register_map_callbacks(df, rt_df, ap_df):
    global hp_df, route_df, airport_df
    hp_df = df
    route_df  = rt_df
    airport_df = ap_df

    @callback(
        Output('interactive-map', 'figure'),
        Input("bar-apply-btn", "n_clicks"), 
        State({"type": "attribute-filter-dropdown", "subtype": "State"}, "value"),
        State({"type": "attribute-filter-dropdown", "subtype": "Event_Type"}, "value"),
        State({"type": "attribute-filter-dropdown", "subtype": "Apparition_Type"}, "value"),
        State({"type": "attribute-filter-dropdown", "subtype": "holiday-dropdown"}, "value"),
        State({"type": "attribute-filter-dropdown", "subtype": "holiday-dropdown"}, "options"),
        State("coloring-toggle", "value"),
        State("size-arg", "value"),
        State("start-year", "value"),
        State("start-month", "value"),
        State("start-day", "value"),
        State("end-year", "value"),
        State("end-month", "value"),
        State("end-day", "value"),
        State('include-start-date', "value"),
        State('include-end-date', "value"), 
        State('airport-type-checklist', "value"),
        State('airport-visibility-checklist', "value"),
        prevent_initial_call=False,
    )
    def update_map(
        n_clicks, 
        state, event_type, apparition_type, holiday, holiday_options, coloring_toggle, size_arg,
        s_year, s_month, s_date, e_year, e_month, e_date,
        s_include, e_include, airport_types, airport_visibility
    ):
        
        triggered_inputs = extract_additional_tags(ctx.states)        
        additional_tags = list(triggered_inputs.keys())

        # if filtering by start date
        if s_include:
            start_date = f"{s_year}-{s_month}-{s_date}"
        else:
            start_date = "1000-1-1"
        # if filtering by end date
        if e_include:
            end_date = f"{e_year}-{e_month}-{e_date}"
        else:
            end_date =  "2025-1-1"

        date_range = [start_date, end_date]

        # define coloring
        if coloring_toggle in list(triggered_inputs.keys()): 
            coloring = {coloring_toggle: triggered_inputs[coloring_toggle]} # if coloring toggle is one of the filtered attributes, set coloring by attribute
        else:
            coloring = {coloring_toggle: get_legend_items(hp_df, coloring_toggle)}  # otherwise get all possible values for that attribute
        
        if holiday == ['all']:
            holiday = [opt['value'] for opt in holiday_options if opt['value'] != 'all']
        
        # Filter Data
        filtered_hp_df = filter_hp_df(hp_df, state, event_type, apparition_type, date_range, holiday)
        filtered_route_df = filter_route_df(filtered_hp_df, route_df)
        filtered_airport_df = filter_airport_df(filtered_hp_df, airport_df, airport_types)
        filtered_hp_df = filtered_hp_df.astype(str)

        return hp_interactive_darkmatter(filtered_hp_df, filtered_route_df, filtered_airport_df, coloring, size_arg, additional_tags, airport_visibility)

    


from itertools import chain
from datetime import date
import regex as re

# Unique Legend Items
def get_legend_items(df_hp, legend_key):

    # return True and False if Bool
    if df_hp[legend_key].dtype == 'bool':
        return ['True', 'False']
    
    s = set().union(*df_hp[legend_key].dropna().str.split(' | ').tolist())
    # remove delimiter if it was caught
    try:
        s.remove('|')  
    except:
        pass

    return  sorted(list(s))
# String to Datetime
def parse_date(s): 
    return date(*map(int, s.split('-'))) 
# Datetime to String
def convert_date_str(date):
    return date.strftime('%Y-%m-%d')
# Date Range Filter
def in_date_range(date_list, start_date, end_date):
    return any(start_date <= date <= end_date for date in date_list)
# Year slider converter
def transform_year(year):
    '''
    Custom hard-coded mapping of years for year-slider. Necessary to fit all years on one slider.
    '''
    # 1600
    if year == 1780:
        return 1600
    # 1650
    elif year == 1785:
        return 1650
    # 1700
    elif year == 1790:
        return 1700
    # 1750
    elif year == 1795:
        return 1750
    return year
# Query "or" regex
def query_df(query_keys, s):

    # Conver to list if single string is passed
    if isinstance(query_keys, str):
        query_keys = [query_keys]

    # Return False if df is null 
    if s is None:
        return False
    # Make logical "or" regex and query
    query_regex = "|".join(map(re.escape, query_keys))
    return bool(re.search(query_regex, s))
# Haunted Places Query
def filter_hp_df(
    hp_df,
    state=None, event_type=None, apparition_type=None, haunt_date_range=None, holiday = None):
    
    filtered_hp_df = hp_df.copy()

    if state:
        filtered_hp_df = filtered_hp_df[filtered_hp_df['State'].apply(lambda s: query_df(state, s))]
    if event_type:
        filtered_hp_df = filtered_hp_df[filtered_hp_df['Event_Type'].apply(lambda s: query_df(event_type, s))]
    if apparition_type:
        filtered_hp_df = filtered_hp_df[filtered_hp_df['Apparition_Type'].apply(lambda s: query_df(apparition_type, s))]
    if haunt_date_range:
        start_date, end_date = map(parse_date, haunt_date_range)
        filtered_hp_df = filtered_hp_df[(filtered_hp_df['Haunted_Places_Date'].apply(lambda x: in_date_range(x, start_date, end_date)))]
    if holiday:
        holiday = list(map(parse_date,holiday))
        filtered_hp_df = filtered_hp_df[filtered_hp_df['Haunted_Places_Date'].apply(lambda x: any([in_date_range(x, h, h) for h in holiday]))]
    
    filtered_hp_df['Haunted_Places_Date'] = filtered_hp_df['Haunted_Places_Date'].apply(lambda x: [convert_date_str(y) for y in x])
    filtered_hp_df = filtered_hp_df.astype(str)

    return filtered_hp_df
# Airports Query
def filter_airport_df(
    filtered_hp_df,
    airport_df,
    flight_intersections,
    airport_intersections,
    airport_types : list = []):

    # if airport_types not specified, use all types
    if 'all' in airport_types:
        airport_types = airport_df['Type'].unique().tolist()
    
    
    filtered_airport_df = airport_df[airport_df['Type'].isin(airport_types)].copy()

    haunted_ids = filtered_hp_df['Haunted_Places_Id'].tolist()

    filtered_flight_intersections = {k: v['Routes'] for k, v in flight_intersections.items() if k in haunted_ids}
    filtered_airport_intersections = {k: v['Airports'] for k, v in airport_intersections.items() if k in haunted_ids}

    relevant_iata_codes = set()
    relevant_airports = set()

    for _, v in filtered_flight_intersections.items():
        relevant_iata_codes.update(
            chain(
            (route['Dest_Airport'] for route in v),
            (route['Source_Airport'] for route in v)
            )
        )
        
    for _, v in filtered_airport_intersections.items():
        relevant_airports.update(airport['Airport_ID'] for airport in v)

    filtered_airport_df = filtered_airport_df[filtered_airport_df['Id'].isin(relevant_airports) | filtered_airport_df['Iata_Code'].isin(relevant_iata_codes)]
    
    return filtered_airport_df
# Routes Query
def filter_route_df(
    filtered_hp_df, 
    route_df, 
    flight_intersections):

    haunted_ids = filtered_hp_df['Haunted_Places_Id'].tolist()

    filtered_flight_intersections = {k: v['Routes'] for k, v in flight_intersections.items() if k in haunted_ids}

    relevant_routes = set()

    for _, v in filtered_flight_intersections.items():
        relevant_routes.update(route['Route_ID'] for route in v)

    filtered_route_df = route_df.loc[list(relevant_routes)]

    return filtered_route_df

# Helper Functions #
import textwrap
import pandas as pd
import json

def filter_used_routes_airports(hp_df, route_df, airport_df):

    # flatten Airport Ids that intersect with a haunted place
    flattened_airports = list(set([x for y in hp_df['Intersecting_Airport_Ids'].values for x in y]))
    # flatten Route Ids that intersect with a haunted place   
    flattened_routes = list(set([x for y in hp_df['Intersecting_Route_Ids'].values for x in y]))
    
    # filter reoutes and airports
    filtered_routes = route_df.loc[flattened_routes].copy()
    filtered_airports = airport_df.loc[flattened_airports].copy()

    return filtered_routes, filtered_airports

def main(hp_df, route_df, airport_df):
'''
    Steps:
        1. Filter out unused columns from hp_df, airport_df, and route_df
        2. Filter out unused routes and airports to save storage
        3. Add Index Names and Save
    Input:
        [hp_df]         - dataframe with features added
        [route_df]       - dataframe of routes
        [airport_df]     - dataframe of airports

    Output:
        './data/airport_df.tab'  - Final hp_df with features added
        './data/airport_df.tab'  - Final airport_df with features added
        './data/route_df.tab'    - Final route_df with features added    
'''

    # Columns Used
    hp_cols = ['City', 'Description', 'State', 'Location', 'Longitude' ,'Latitude', 'Audio_Evidence', 
    'Visual_Evidence', 'Haunted_Places_Date', 'Haunted_Places_Witness_Count', 'Event_Type',
    'Aerodrome_Count', 'Aerodrome_Proximity', 'Flight_Intersection_Count',
    'Flight_HighTraffic', 'Apparition_Type', 'Time_of_Day'] 

    # Filter out columns used
    hp_df_out = hp_df[hp_cols].copy()

    # Format description textbox for web
    hp_df_out['Description'] = hp_df_out['Description'].apply(
            lambda x: "<br>".join(textwrap.wrap(x, width=50))
        )

    # copy airport_df
    airport_cols = ['Type', 'Name', 'Latitude_Deg', 'Longitude_Deg', 'Iata_Code', 'Airport_Radius'] 
    # filter out unused columns
    airport_df_out = airport_df[airport_cols].copy()
    airport_df_out.index.name = 'Airport_ID'

    # copy route df
    route_cols = ['Source_Airport', 'Destination_Airport', 'Flight_Path']
    # filter out unused columns
    route_df_out = route_df[route_cols].copy()
    route_df_out.index.name = 'Route_ID'

    # filter out unused routes and airports
    route_df_out, airport_df_out = filter_used_routes_airports(hp_df_out, route_df_out, airport_df_out)

    ## Save ##
    airport_df_path, route_df_path = './data/airport_df.tab', './data/route_df.tab'

    route_df_out.to_csv(route_df_path, sep = '\t', index = False) # Routes

    airport_df_out.to_csv('./data/df_airports.csv', sep = ',', index = False) # Airports
    csv.writer(airport_df_path, dialect='excel-tab').writerows(csv.reader('./data/airline_airports.csv')) # Convert to .tab
    os.remove('./data/df_airports.csv')

    hp_df.to_csv('./data/hp_df.tab', sep = '\t', index = False) # Haunted PLaces

    print(f"Haunted Places df saved at: `./data/hp_df.tab`", f"Airport df saved at: `{airport_df_path}`", f"Route df saved at: `{route_df_path}`", )

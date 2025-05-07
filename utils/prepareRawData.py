# Helper Functions #
import textwrap
import pandas as pd
import json

def add_route_id_col(hp_df, route_intersections):
    '''
    Adds "Intersecting_Route_Ids" column to hp_df. Entries are lists of indices coressponding to routes_df
    '''
    hp_df['Intersecting_Route_Ids'] = None
    hp_df['Intersecting_IATA_Codes'] = None
    # iterate through haunted place ids in intersection data
    for hp_idx in route_intersections.keys():
        
        # add intersecting route to list
        intersecting_routes = []
        intersecting_iata_codes = []

        
        for route in route_intersections.get(hp_idx)['Routes']:
            # add index corresponding to 'routes_df'
            intersecting_routes.append(route['Route_ID'])
            # add iata codes correspondng to 'airports_df'
            intersecting_iata_codes.append(route['Dest_Airport'])
            intersecting_iata_codes.append(route['Source_Airport'])
        # filter out duplicates
        intersecting_iata_codes = list(set(intersecting_iata_codes))
        
        # add both columns to df
        hp_df.at[int(hp_idx),'Intersecting_Route_Ids'] = intersecting_routes
        hp_df.at[int(hp_idx),'Intersecting_IATA_Codes'] = intersecting_iata_codes

    return hp_df


def add_airport_id_col(hp_df, airport_intersections, airport_df):
    '''
    Adds "Intersecting_Airport_Ids" column to hp_df. Entries are lists of indices coressponding to airport_df
    '''
    hp_df['Intersecting_Airport_Ids'] = None
    # iterate through haunted place ids in intersection data
    for hp_idx in airport_intersections.keys():
        # add intersecting airport to list
        intersecting_airports = []
        for airport in airport_intersections.get(hp_idx)['Airports']:
            intersecting_airports.append(airport['Airport_ID'])
        # add indices of airports with matching iata codes 
        intersecting_iata_codes = hp_df.loc[int(hp_idx), 'Intersecting_IATA_Codes'] 
        airports_used_in_flights = airport_df.loc[airport_df['Iata_Code'].isin(intersecting_iata_codes)].index.tolist()
        [intersecting_airports.append(idx) for idx in airports_used_in_flights]

        # remove duplicates
        intersecting_airports = list(set(intersecting_airports))

        # add all indices to df
        hp_df.at[int(hp_idx),'Intersecting_Airport_Ids'] = intersecting_airports

    # remove iata codes column
    return hp_df


def filter_used_routes_airports(hp_df, route_df, airport_df):

    # flatten Airport Ids that intersect with a haunted place
    flattened_airports = list(set([x for y in hp_df['Intersecting_Airport_Ids'].values for x in y]))
    # flatten Route Ids that intersect with a haunted place   
    flattened_routes = list(set([x for y in hp_df['Intersecting_Route_Ids'].values for x in y]))
    
    # filter reoutes and airports
    filtered_routes = route_df.loc[flattened_routes].copy()
    filtered_airports = airport_df.loc[flattened_airports].copy()

    return filtered_routes, filtered_airports
## Load Raw Data

# Haunted Places 
hp_df = pd.read_csv("./data/haunted_places_features_added_v2.tab", sep="\t", index_col = 'Haunted_Places_Id')
hp_df['Haunted_Places_Date'] = hp_df['Haunted_Places_Date'].apply(lambda x: eval(x)) 
# Routes  
route_df = pd.read_csv("./data/american_routes.tsv", sep="\t")
route_df["Flight_Path"] = route_df["Flight_Path"].apply(lambda x: eval(x) if isinstance(x, str) else x)
# Airports 
airport_df = pd.read_csv("./data/american_airports.tsv", sep="\t")
airport_df["Airport_Radius"] = airport_df["Airport_Radius"].apply(lambda x: eval(x) if isinstance(x, str) else x)
# Flight Intersections 
with open("./data/flight_proximity_data.json", "r") as f:
    flight_intersections = json.load(f)
# Airport Intersections
with open("./data/airport_proximity_data.json", "r") as f:
    airport_intersections = json.load(f)



# hp_df
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

# Add route and airport index columns
hp_df_out = add_route_id_col(hp_df_out, flight_intersections)
hp_df_out = add_airport_id_col(hp_df_out, airport_intersections, airport_df)

# remove redundant column with IATA codes from hp_df
hp_df_out.drop('Intersecting_IATA_Codes', axis = 1, inplace = True)

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

# save 
route_df_out.to_csv('./data/route_df.tab', sep = '\t', index = True)
airport_df_out.to_csv('./data/airport_df.tab', sep = '\t', index = True)
hp_df_out.to_csv('./data/hp_df.tab', sep = '\t', index = True)

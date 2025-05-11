# System Path #
import os
import sys, csv
from io import StringIO
import requests
import json

# Pandas #
import pandas as pd

# Runtime #
from tqdm import tqdm 

# Flight Trajectory Functions #
from dsci_550_a1.flightFunctions import *

def load_airport_df():
    # OurAirports #
    airports_url = "https://davidmegginson.github.io/ourairports-data/airports.csv"
    response = requests.get(airports_url)

    columns = ['Id','Ident','Type','Name','Latitude_Deg','Longitude_Deg','Elevation_Ft','Continent','Iso_Country','Iso_Region','Municipality','Scheduled_Service',
            'Icao_Code','Iata_Code','Gps_Code','Local_Code','Home_Link','Wikipedia_Link','Keywords']


    airport_df = pd.read_csv(StringIO(response.text), header=None, names = columns, index_col= False)

    # Filter American Airports #
    airport_df = (airport_df
                        .loc[(airport_df["Iso_Country"] == "US") & (airport_df["Type"] != "closed")]
                        .drop(["Continent", "Wikipedia_Link", "Keywords", "Home_Link"], axis = 1)
                        .fillna({
                            "Iata_Code": 0,
                            "Icao_Code": 0,
                            "GPS_Code": 0,
                            "Local_Code": 0
                        })
                        .astype({
                            "Name": str,
                            "Iata_Code": str,
                            "Icao_Code": str,
                            "Gps_Code": str,
                            "Local_Code": str,
                            "Latitude_Deg": float,
                            "Longitude_Deg": float,
                            "Elevation_Ft": float,  
                        }
                        )
                        .reset_index(drop=True)  
    )
    return airport_df

def load_route_df():
# OpenFlights #
routes_url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"
response = requests.get(routes_url)

columns = ["Airline","Airline_ID","Source_Airport","Source_Airport_ID","Destination_Airport","Destination_Airport_ID","Codeshare","Stops","Equipment"]

route_df = pd.read_csv(StringIO(response.text), header=None, names = columns, index_col= False)

return route_df

def process_and_merge(airport_df, route_df)
    '''
    Steps:
    1. Calculate Airport radius of influence "d" and circular coordinates for plot as "Airport_Radius". 
    2. Add coordinates for source and destination airports from "airport_df" using pd.merge(). 
    3. drop unused columns
    '''
    airport_proximity_dict = {
        "large_airport" : 55560,    # 30 nautical miles
        "medium_airport" : 9260,    # 5 nautical miles
        "small_airport" : 5556,     # 3 nautical miles
        "heliport":  2778,          # 1.5 nautical miles
        "seaplane_base" : 5556,     # 3 nautical miles
        "balloonport" : 5556        # 3 nautical miles
    }

    # Generate Interpolated Airport Radius Using `generate_circle` from `utils.flightFunctions`#
    airport_df["Airport_Radius"] = airport_df.apply(lambda row: generate_circle([row['Latitude_Deg'],row['Longitude_Deg']], r = airport_proximity_dict[row['Type']],  n = 10), axis = 1)
    airport_df['d'] = airport_df.apply(lambda row: airport_proximity_dict[row['Type']], axis = 1)

    # Filter Routes with Source and Destination in US #
    american_Iata_Codes = airport_df.loc[airport_df['Iata_Code'] != '0', 'Iata_Code'].to_list()
    route_df = route_df[route_df['Source_Airport'].isin(american_Iata_Codes) & route_df['Destination_Airport'].isin(american_Iata_Codes)]

    # Add Source and Destination Airport #
    route_df = route_df.merge(airport_df[["Latitude_Deg","Longitude_Deg","Type", "Iso_Country","Iata_Code"]],
                        left_on = "Source_Airport", 
                        right_on = "Iata_Code",
                        how = 'left',
                        ).rename({"Latitude_Deg": "Latitude_Source", "Longitude_Deg" : "Longitude_Source", "Type" : "Type_Source", "Iso_Country": "Country_Source"}, axis = 1)

    route_df = route_df.merge(airport_df[["Latitude_Deg","Longitude_Deg","Type", "Iso_Country","Iata_Code"]],
                        left_on = "Destination_Airport", 
                        right_on = "Iata_Code",
                        how = 'left',
                        ).rename({"Latitude_Deg": "Latitude_Dest", "Longitude_Deg" : "Longitude_Dest", "Type" : "Type_Dest", "Iso_Country": "Country_Dest"}, axis = 1)

    # Drop columns created in merge #
    route_df.drop(["Iata_Code_x", "Iata_Code_y", 'Stops', 'Codeshare', 'Source_Airport_ID', 'Airline_ID', "Country_Source", "Country_Dest"], axis = 1, inplace = True)

    # Add Interpolated flight path #
    route_df["Flight_Path"] = route_df.apply(lambda row: flight_trajectory([row['Latitude_Source'],row['Longitude_Source']], [row['Latitude_Dest'], row['Longitude_Dest']], n = 10), axis = 1)

    print("\nFlight datasets processed and joined. Now calculating intersections with `hp_df`...")

    return route_df, airport_df

def add_flight_features(route_df, airport_df, hp_df): 
    '''
    Input:
        [hp_df]         - dataframe of haunted places
        [route_df]       - dataframe of routes
        [airport_df]     - dataframe of airports
    Return:
        [hp_df*]         - dataframe with features added
        [route_df]       - dataframe of routes
        [airport_df]     - dataframe of airports
    Steps:
    1. Calculate intersecting routes. 
    2. Calculate intersecting airports and add airports used in intersecting routes.
    3. Count number of each type of intersection and add boolean features and save.

    NOTE:
        - Uses functions from utils.flightFunctions.py
    '''
    tqdm.pandas(desc = "Calculating Route Intersections.")

    p2s = route_df["Flight_Path"]
    ds = [10000] * len(p2s)
    hp_df["Intersecting_Route_Ids"] = hp_df.apply(lambda x: calculate_intersections(x, p2s, ds), axis = 1)

    print("Indicies stored in `Intersecting_Airport_Ids` column of `hp_df`.")
    print("\nIntersections calculated.\nNow adding [`Aerodrome_Count`, `Aerodrome_Proximity`, `Flight_Intersection_Count`, `Flight_HighTraffic`] columns...")

    # Airports #
    tqdm.pandas(desc = "Calculating Airport Intersections.")

    p2s = list(zip(airport_df["Latitude_Deg"], airport_df["Longitude_Deg"]))
    ds = list(airport_df['Type'].map(lambda x: airport_proximity_dict[x]))
    hp_df["Intersecting_Airport_Ids"] = hp_df.progress_apply(lambda x: calculate_intersections(x, p2s, ds), axis = 1)

    add_airports_used_in_flights(hp_ds, route_df, airport_df) # Adding airports that are sources and destinations in routes 
    print("Indicies stored in `Intersecting_Airport_Ids` column of `hp_df`")


    hp_df['Aerodrome_Count'] = hp_df["Aerodrome_Intersections"].apply(lambda x : len(x))
    hp_df['Aerodrome_Proximity'] = hp_df["Aerodrome_Count"] > 0 

    hp_df['Flight_Intersection_Count'] = hp_df["Flight_Intersections"].apply(lambda x : len(x))
    hp_df['Flight_HighTraffic'] = hp_df["Flight_Intersection_Count"] > 10

    return hp_df, route_df, airport_df   

def main(hp_df):
'''
    Input:
        [hp_df]         - dataframe of haunted places

    Output:
        [hp_df*]         - dataframe with features added
        [route_df]       - dataframe of routes
        [airport_df]     - dataframe of airports

    Features Added to hp_df:
        [Intersecting_Route_Ids]    - indicies of route_df that intersect with a haunted place
        [Intersecting_Airport_Ids]  - indicies of airport_df that intersect with a haunted place
        [Aerodrome_Count]           - number of airports that intersect with a haunted place
        [Aerodrome_Proximity]       - True if at least one airport intersects with a haunted place
        [Flight_Intersection_Count] - number of routes that intersect with a haunted place
        [Flight_HighTraffic]        - True if at least 10 routes intersects with a haunted place
'''
    airport_df = load_airport_df()
    route_df = load_route_df()
    airport_df, route_df = process_and_merge(airport_df, route_df)
    
    return add_flight_features(hp_df, route_df, airport_df)

if __name__ == "__main__":
    main(hp_df)
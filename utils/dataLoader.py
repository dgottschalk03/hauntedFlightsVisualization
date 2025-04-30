import pandas as pd
from datetime import date
import ast
import json
import os
import base64

# Date parsing helper
def parse_date(s): 
    return date(*map(int, s.split('-'))) 

# Load Data
def load_all_data():
    # Haunted Places 
    hp_df = pd.read_csv("./data/haunted_places_features_added_v2.tab", sep="\t")
    hp_df['Haunted_Places_Date'] = hp_df['Haunted_Places_Date'].apply(lambda x: ast.literal_eval(x)) 
    hp_df['Haunted_Places_Date'] = hp_df['Haunted_Places_Date'].apply(lambda x: [parse_date(y) for y in x] if isinstance(x, list) else x)
    # Routes  
    route_df = pd.read_csv("./data/american_routes.tsv", sep="\t")
    route_df["Flight_Path"] = route_df["Flight_Path"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    # Airports 
    airport_df = pd.read_csv("./data/american_airports.tsv", sep="\t")
    airport_df["Airport_Radius"] = airport_df["Airport_Radius"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    # Flight Intersections 
    with open("./data/flight_proximity_data.json", "r") as f:
        flight_intersections = json.load(f)
    # Airport Intersections
    with open("./data/airport_proximity_data.json", "r") as f:
        airport_intersections = json.load(f)

    return (
        hp_df,
        route_df,
        airport_df,
        flight_intersections,
        airport_intersections
    )
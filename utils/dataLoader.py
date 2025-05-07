import pandas as pd
from utils.query import parse_date

# Load Data
def load_all_data():
    '''
    Load all datasets for plotly pages. Meant to be run from scripts in 'pages' directory.
    '''
    # Haunted Places 
    hp_df = pd.read_csv("./data/hp_df.tab", sep="\t")
    
    # convert haunted place dates to list of datetimes
    hp_df['Haunted_Places_Date'] = hp_df['Haunted_Places_Date'].apply(lambda x: eval(x)) 
    hp_df['Haunted_Places_Date'] = hp_df['Haunted_Places_Date'].apply(lambda x: [parse_date(y) for y in x] if isinstance(x, list) else x)
    
    # convert intersecting airport and route ids to lists of integers
    hp_df['Intersecting_Airport_Ids'] = hp_df['Intersecting_Airport_Ids'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    hp_df['Intersecting_Route_Ids'] = hp_df['Intersecting_Route_Ids'].apply(lambda x: eval(x) if isinstance(x, str) else x)

    # Routes  
    route_df = pd.read_csv("./data/route_df.tab", sep="\t", index_col = 'Route_ID')
    route_df["Flight_Path"] = route_df["Flight_Path"].apply(lambda x: eval(x) if isinstance(x, str) else x)
    
    # Airports 
    airport_df = pd.read_csv("./data/airport_df.tab", sep="\t", index_col = 'Airport_ID')
    airport_df["Airport_Radius"] = airport_df["Airport_Radius"].apply(lambda x: eval(x) if isinstance(x, str) else x)

    return hp_df, route_df, airport_df

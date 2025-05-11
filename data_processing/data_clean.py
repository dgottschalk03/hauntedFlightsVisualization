# System Path #
import os
import sys 

# Pandas, json and runtime #
import pandas as pd
import json
import string

# Stopword Cleaning using NLTK #
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# Reading CSV
input_path = "./data/raw/haunted_places.tab"

df = pd.read_csv(input_path, sep = "\t")

## Fill Missing Descriptions
df["description"] = df["description"].fillna('').astype(str)

## Impute missing city and location ##

# Read Description
df.loc[4082, 'city'] = "Maumee"
# Looked up "michigan haunted theater 2005 and found it was in Grand Haven"
df.loc[176, 'city'] = "Grand Haven"
df.loc[176, 'city_longitude'] = 86.2284
df.loc[176, 'city_latitude'] = 43.0631

# Entry takes place in Florida. Description and were incorrectly separated.
df.loc[9465, 'city'] = "Miami"
df.loc[9465, 'description'] = df.loc[9465, 'description'] + df.loc[9465, 'location']
df.loc[9465, 'location'] = 'cemetary'

# Read Descriptions and filled location NAN Values
df.loc[2427, 'location'] = "Bodega Bay"
df.loc[2756, 'location'] = "Elsinore Middle School"
df.loc[4712, 'location'] = "Dolly Field"


## Impute Missing Longitude and Latitude ##

# Fill NAN Longitude values with city longitude
df.loc[df['longitude'].isna(), 'longitude'] = df[df['longitude'].isna()]['city_longitude']

# Fill NAN latitude values with city latitude
df.loc[df['latitude'].isna(), 'latitude'] = df[df['latitude'].isna()]['city_latitude']

# Fill NAN city_longitude values with longitude if it exists
df.loc[df['city_longitude'].isna(), 'city_longitude'] = df[df['city_longitude'].isna()]['longitude']

# Fill NAN city_latitude values with latitude if it exists
df.loc[df['city_latitude'].isna(), 'city_latitude'] = df[df['city_latitude'].isna()]['latitude']


## Filling last of coordinates with coordinates of state ##
state_coordinates_list = {
    'PA': {'Latitude': 41.2033, 'Longitude': -77.1945},
     'AR': { 'Latitude': 34.7465, 'Longitude': -92.2896},
     'AL': { 'Latitude': 32.3182, 'Longitude': -86.9023},
     'OH': { 'Latitude': 40.4173, 'Longitude': -82.9071},
     'ND': { 'Latitude': 47.5515, 'Longitude': -101.002},
     'ND': { 'Latitude': 47.5515, 'Longitude': -101.002},
     'KS': { 'Latitude': 39.0119, 'Longitude': -98.4842},
     'IL': { 'Latitude': 40.6331, 'Longitude': -89.3985},
     'IN': { 'Latitude': 40.2672, 'Longitude': -86.1349},
     'IN': { 'Latitude': 40.2672, 'Longitude': -86.1349},
     'VA': { 'Latitude': 37.4316, 'Longitude': -78.6569},
     'GA': { 'Latitude': 32.1656, 'Longitude': -82.9001},
     'FL': { 'Latitude': 27.9944, 'Longitude': -81.7603},
     'MN': { 'Latitude': 46.7296, 'Longitude': -94.6859}
}

for idx in df.loc[df['latitude'].isna()].index:
    state = df.loc[idx, 'state_abbrev']
    df.loc[idx, "latitude"] = state_coordinates_list[state]['Latitude']
    df.loc[idx, "longitude"] = state_coordinates_list[state]['Longitude']
    df.loc[idx, "city_longitude"] = state_coordinates_list[state]['Longitude']
    df.loc[idx, "city_latitude"] = state_coordinates_list[state]['Latitude']


df_cleaned = df.copy()

extracted_descriptions = list(map(lambda x: x.lower().strip(), df['description'].to_list()))
extracted_descriptions

nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words("english"))

# Keep "I" and "We". These are used for Haunted_Places_Witness_Count feature. #
stop_words.discard('i') 
stop_words.discard('we')

for i in range(len(extracted_descriptions)):
    description = extracted_descriptions[i]
    
    # Only Add Non-Stopwords and Non-Punctuation Tokens (keep periods) #
    description = " ".join([word.lower().strip() for word in word_tokenize(description.replace('.', '. ')) if (word not in stop_words) and (word not in string.punctuation.replace('.',''))])
    df_cleaned.loc[i, 'description'] = description


# edge case (all stopwords) #
df_cleaned.loc[1063, "description"] = "" 

# Set index #
df_cleaned["Haunted_Places_Id"] = df_cleaned.index # dataset without stopwords (used for feature extraction)
df['Haunted_Places_Id'] = df.index # dataset w/ stopwords (used for storing features)

# capitalize column names #
cols = ['City',
 'Country',
 'Description',
 'Location',
 'State',
 'State_Abbrev',
 'Longitude',
 'Latitude',
 'City_Longitude',
 'City_Latitude',
 'Haunted_Places_Id']

df_cleaned.columns = cols
df.columns = cols

## Save outputs ##
outDir = "../processed/"
os.makedirs(outDir, exist_ok=True)

# Feature Storage df #
outfile = os.path.join(outDir, "hp_df.tab") 
print(f"saving to {outfile}.\nThis data is used for storing added features.")
df.to_csv(outfile, sep = "\t", index = False)
print("\n")

# Feature Generation df #
outfile = os.path.join(outDir, "hp_df_cleaned.tab")
print(f"saved to '{outfile}'.\nThis data is used for feature extraction.")
df_cleaned.to_csv(outfile, sep = "\t", index = False)
print("\n")
print("Data Cleaning Done!")
import pandas as pd
import re 
import time
import json
import datetime
from feature_extraction_helpers import contains_keywords, extract_dates



output_path = "./data/processed/hp_df.tab"
input_path = "./data/raw/hp_df_cleaned.tab"

# Reading CSVs
df_input = pd.read_csv(f"{input_path}", sep = "\t")
df_output = pd.read_csv(f"{output_path}", sep = "\t")

# Feature Names
feature_names = ["Audio_Evidence", "Visual_Evidence", "Haunted_Places_Date", ]



# Define Audio Keyword List
keywords = json.load(open("../data/keywords/keywords.json"))
audio_keywords = keywords["Verbs"]["Audio"] + keywords["Nouns"]["Audio"] + keywords["Descriptors"]["Audio"]
visual_keywords = keywords["Verbs"]["Visual"] + keywords["Nouns"]["Visual"] 

## Feature Extraction ##
start = time.time()

## Audio and Visual Evidence ##
df_output["Audio_Evidence"] = df_input["Description"].apply(contains_keywords, args = (audio_keywords))  
df_output["Visual_Evidence"] = df_input["Description"].apply(contains_keywords, args = (visual_keywords)) 

## Haunted Places Date ##
# NOTE: I extract dates using both cleaned and uncleaned "descriptions". Then Combine the two. This got the best results. 

df_output["Haunted_Places_Date_Cleaned"] = df_input["Description"].apply(extract_dates)
df_output["Haunted_Places_Date_Raw"] = df_output["Description"].apply(extract_dates)

# Combine cleaned and raw into one final column
df_output["Haunted_Places_Date"] = (df_output
    # Combine cleaned and raw
    .apply(lambda x: x['Haunted_Places_Date_Cleaned']['dates'] +  x['Haunted_Places_Date_Raw']['dates'], axis = 1)
    # Remove Duplicates
    .apply(lambda x: list(set(x)))
    # remove [2025, 1, 1] if there are any valid dates
    .apply(lambda x: clean_dates(x))
)

df_output = df_output.drop(["Haunted_Places_Date_Cleaned", "Haunted_Places_Date_Raw"], axis = 1)

df_output["Haunted_Places_Date"] = (df_output["Haunted_Places_Date"].apply(lambda x : x[0] if isinstance(x, list) else x))
df_output['Haunted_Places_Date'] = pd.to_datetime(df_output['Haunted_Places_Date'], errors='coerce').dt.date
df_output["Haunted_Places_Date"].fillna(datetime.date(2025,1,1), inplace = True)

##

witness_nouns = keywords["Nouns"]["Witness"]
witness_verbs = keywords["Verbs"]["Witness"]



end = time.time()


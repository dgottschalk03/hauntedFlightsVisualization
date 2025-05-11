import pandas as pd
import re 
import time
import json
import datetime
from tqdm import tqdm
from number_parser import parse # https://github.com/scrapinghub/number-parser
from feature_extraction_helpers import *


# Init Paths
output_path = "./data/processed/hp_df.tab"
input_path = "./data/raw/hp_df_cleaned.tab"

# Reading CSVs
df_input = pd.read_csv(f"{input_path}", sep = "\t")
df_output = pd.read_csv(f"{output_path}", sep = "\t")

# Feature Names
feature_names = ["Audio_Evidence", "Visual_Evidence", "Haunted_Places_Date", "Haunted_Places_Witness_Count", "Event_Type",]



## Keywords ##
keywords = json.load(open("../data/keywords/keywords.json"))

audio_keywords = keywords["Verbs"]["Audio"] + keywords["Nouns"]["Audio"] + keywords["Descriptors"]["Audio"]
visual_keywords = keywords["Verbs"]["Visual"] + keywords["Nouns"]["Visual"] 

witness_nouns = keywords["Nouns"]["Witness"]
witness_verbs = keywords["Verbs"]["Witness"]

event_groups = {}
for key, patterns in keywords["Precompiled_Regex"].items():
    if key == "Apparitions":
        apparition_groups = {k: [recompile_regex(v)] for k, v in patterns.items()}
    elif key == "Time_Of_Day":
        time_of_day_groups = {k: [recompile_regex(v)] for k, v in patterns.items()}
    else:
        event_groups[key] = recompile_regex(patterns)

## Feature Extraction ##
t_start = time.time()

# Audio and Visual Evidence #
df_output["Audio_Evidence"] = df_input["Description"].apply(contains_keywords, args = (audio_keywords))  
df_output["Visual_Evidence"] = df_input["Description"].apply(contains_keywords, args = (visual_keywords)) 

# Haunted Places Date #
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

# Witness Count #

# Parse numbers and ordinals #
parsed_decriptions = df_input["Description"].progress_apply(parse)
parsed_descriptions = parsed_decriptions.progress_apply(parse_ambiguous_quantifiers)

# Extract Eyewitness Count #
df_output["Haunted_Places_Witness_Count"] = [
    extract_eyewitness_counts((entry))
    for entry in tqdm(parsed_decriptions, desc = "Extracting Eyewitness Counts")
]
df_output["Haunted_Places_Witness_Count"] = df_output["Haunted_Places_Witness_Count"].apply(lambda x: x[0])

# match keyword groups using `match_groups` # 
df_output["Event_Type"] = df_input["Description"].apply(lambda x: match_groups(x, event_groups))
df_output["Apparition_Type"] = df_input["Description"].apply(lambda x: match_groups(x, apparition_groups))
df_output["Time_Of_Day"] = df_input["Description"].apply(lambda x: match_groups(x, apparition_groups))


t_end = time.time()

print("-" * 150, "Feature Extraction Complete", "-" * 150)
print(f"Time Elapsed: {(t_end - t_start):.2f} secconds")

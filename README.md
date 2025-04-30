# DSCI_550_Assignment_README

## Group Members
<div align="center">

| Name             | Initials |
|------------------|----------|
| Daniel Gottschalk| [dg]     |
| Reha Matai       | [rm]     |
| Serafina Smith   | [ss]     |
| Mikena Moore     | [mm]     |
| Kate Mathew      | [km]     |

</div>

**Quick links:**
  - :point_right: [A1](#dsci_550_a1) 
  - :point_right: [A2](#dsci_550_a2) 

---
# DSCI_550_A1

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Analysis of the Haunted Places Dataset. Assignment 1 for DSCI_550 SP 25. 

Due | 3-14-2025

[Reference](./references/DSCI550_HW_BIGDATA_HAUNTED.pdf)
    


## Project Organization

```
├── README.md          <- The top-level README.
|
├── clones             <- Store cloned ettlib and tika-similarity repos 
│
├── clustering         <- Clustring output 
│
├── data
│   ├── joined_datasets<- Datasets joined to haunted_features
│   ├── keywords       <- Keywords used in feature extraction. Used in notebooks [1.01, 1.02, 1.04, 1.05, 1.08]
│   ├── processed      <- The final, canonical data sets for modeling. Also includes intermediary da
│   |   |
|   │   ├── *features_added.tab | final dataset 
|   │   ├── *cleaned.tab        | og dataset with stopwords removed and NAN values filled
|   |   ├── *flight*.json       | jsons used for html visualization in notebooks [3.01-3.03]
│   |── raw            <- The original haunted places dataset
│   └── Tika-Similarity<- Stores outputs for tsv2json and conf files used in clustering.
│
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, dataset used, and a short `_` delimited description.
|                         Fields delimited by '-'. e.g.
│                         `1.0-jqp-dataset_1-data_exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         dsci_550_a1 and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Final Report
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── environment.yml    <- Conda environment used to run notebooks 
|
├──  python_3_10.yml    <- Conda environment to run tika-similarity and ettlib (python > 3.10 not supported)
│                         
│
└── dsci_550_a1   <- Source code for use in this project.
    │
    ├── __init__.py                    <- Makes dsci_550_a1 a Python module
    │
    ├── clusterHelper.py               <- Helper function to compute similarity .csvs
    │
    ├── clusterWorkflow.py             <- Script to run full cluster workflow using tika-similarity and ettlib
    │
    ├── flightFunctions.py             <- Flight functions [notebooks 2.01, 3.01-3.03]
    |
    ├── haunteddateday.py              <- Script used to generate haunted_place_time_of_day
    |
    ├── add_daylight_data_columns.py   <- Script used to join Daylight_Duration_Hours
    |
    │
    ├── csv2tab                        <-  Used to convert initial dataset from .csv to .tab
    |
    ├── parsingFunctions.py            <- Functions used for parsing [notebooks 1.01-1.05]
    |
    |    - extractSequences   | sequences tokens by sentences 
    |    - check_regex        | check precompiled regex pattern
    |    - extract_dates      | calculated "Haunted_Places_Date" 
    |    - clean_dates        | Remove invalid dates
    |
    ├── unpack_circles.py              <- Unpacks */circles.json and */cluster.json from clusterWorkflow.py
    |
    |   - unpack_cluster     | returns cluster names and haunted places indicies in said cluster.
│
│
│
```

---


## Naming Conventions for Notebooks
Adapted from [cookie cutter datascience guidelines](https://cookiecutter-data-science.drivendata.org/using-the-template/)

Example Name: **01.01-dg-haunted_places-audio-evidence.ipynb**
- **phase** | 1.01
- **initials** | dg
- **data** | haunted_places
- **description** | audio_evidence

Name of notebooks have 3 parts:


### **0.01** - Phase.Notebook
- 'Phase':  The phase of the analysis
- 'NOTEBOOK': The Nth notebook in that phase to be created.

### **pjb** (Initials of Coder)
Ensures authors get credit. Prevents collisions in coding as well.

### **data-description**
All descriptions written in snake_case
- 'data': Dataset Used
- 'description': Purpose of Notebook



## **Project Overview**

Click on contributor's initials to see file. 

0. **Data Exploration**
- fillNAN and Cleaining | [dg](notebooks/0.01-dg-raw_data-fillna_init_output.ipynb)
- Stopword Cleaning | [dg](notebooks/0.02-dg-raw_data-data_cleaning.ipynb)


1. **Haunted Feature Creation**
Features from Assignment:

- Audio Evidence | [dg](notebooks/1.01-dg-haunted_places-audio_features.ipynb)
- Visual/Video Evidence | [dg](notebooks/1.02-dg-haunted_places-visual_features.ipynb)
- Haunted Places Date | [dg](notebooks/1.03-dg-haunted_places-date_features.ipynb)
- Haunted Places Witness Count | [dg](notebooks/1.04-dg-haunted_places-witness_features.ipynb)
- Event Type | [rm_dg](notebooks/1.05-dg_rh-haunted_places-events_type.ipynb)
- Aparition Type | [rm](notebooks/1.06-rm-haunted_places-apparition_type.ipynb)
- Time of Day | [rm](notebooks/1.07-rm-haunted_places-time_of_day.ipynb) 


2. **Joining Datasets**
- [OpenFlights](https://openflights.org/data.php#route) and [OurAirports](https://ourairports.com/data/) | [dg](notebooks/2.01-dg-airports_data-joining.ipynb)
    - **MIME TYPE** | *Multi-Part/\**
    - **Features** | *{Aerodrome_Count, Aerodrome_Proximity, Flight_Intersection_Count, Flight_HighTraffic}*
- [Place_Of_Worship](https://hub.arcgis.com/datasets/openstreetmap::openstreetmap-places-of-worship-for-north-america/about) | [ss](/notebooks/2.02-ss-Places_of_Worship-joining.ipynb)
    - **MIME TYPE** | *Application/\**
    - **Features** | *{Distance_to_Nearest_Worship, Haunted_Place_Proximity, Religion_Intersection}*
- [BRFFS_Mental_Health]() | [ss](notebooks/2.03-ss-mental_health_data-joining.ipynb)
    - **MIME TYPE** | *Text/\**
    - **Features** | *{Average_Mental_Health_Days, Average_Poor_Health_Days, Depression_Prevalence}*
- [Alcohol_Dataset](https://drugabusestatistics.org/alcohol-abuse-statistics/) | [rm](notebooks/2.02-rm-alcohol_abuse-join.ipynb)
- [Daylight_Hours_Dataset](https://sunrise-sunset.org/api) | [km](./dsci_550_a1/haunteddateday.py)

3. **Visualizations**
- [Airborne_Events.html](notebooks/3.01-dg-haunted_places-airborne_events_plot.ipynb) | [dg]
    - Plot generated using plotly.go
    - Plots 199 haunted places with their intersecting routes and airports
    - All haunted places flagged with either *{Plane_Crash, Electronic_Malfunction, Flying_Object}*
    - Uncomment last line to write html file
- [mostHauntedAirports.html](notebooks/3.02-dg-HP_Features_Added-haunted_airports_plot.ipynb) | [dg]
    - Plots 10 most haunted airplane routes
    - Plots 10 most haunted airports of each type
    - Plots every haunted event color coded by apparition type


4. **Clustering/Inference**
- Clustering Flight Features | [dg](notebooks/4.01-dg-HP_Features_Added-Flight_Clusters.ipynb)
- Clustering Religion Features | [sm_rm](notebooks/4.02-ss_rm-haunted_places_features-religion_cluster.ipynb)
- Clustering Mental Health Features | [sm_rm](notebooks/4.03-ss_rm-haunted_places_features-mental_health_cluster.ipynb)
- Clustering Alcohol Features | [sm_rm](notebooks/4.04-ss_rm-haunted_places_features-alcohol_cluster.ipynb)
- Clustering using [Apparition_Type, Event_Type, and Time_of_Day] as features |  [mm](clustering/mikenaClustering)
-  Clustered using Tika Similarity on ["Time_of_Day", "Total_Deaths", "Apparition_Type", "Daylight_Duration_Hours", "Haunted_Places_Witness_Count", "Event_Type", "Haunted_Place_Proximity"] | [km](clustering/kateClustering)

## **Report and Other Contributions**
**dg**
- wrote **Open Flights Results** and **Open Flights** portions of report

**km**
- Wrote portion of the report on daylight duration and time of day effects on paranormal experiences
- Conducted in-depth analysis of whether murders occur more frequently in the evening
Identified distinct daylight preferences for different apparition types
- Found statistically significant relationship between time of day and evidence types
- Conducted seasonal analysis revealing % of haunting reports occur in winter
- Created visualizations showing the relationships between daylight duration, time of day, apparition types, and evidence patterns [see figures](reports/figures/apparition_type_figs)

**mm**
- Wrote portion of the report about the Apparatition features
- Wrote portion of the report about correlations between keywords and Apparition types 
- Wrote portion of the report about the co-occurring features and locations
- Wrote portion of report introducing and describing the datasets

**rm**
- Wrote portion of report about the Alcohol Abuse related clusters and discussed which locations more likely to be influenced by alcohol abuse that cause more Haunted Places to be reported
- Wrote portion of report about pros/cons of Apache Tika

**ss**
- Wrote portion of report about how the Mental Health related features were extracted and about the clusters.
- Wrote portion of report about how the Places of Worship related features were extracted and about the clusters.

### **Other Contributions**

**dg**
- Project manager
    - wrote README.md
    - organized github and directories
- Wrote [cluster workflow functions](dsci_550_a1/clusterWorkflow.py) [helper functions](dsci_550_a1/clusterHelper.py) used by group to perform clustering
- Wrote [report](plotlyVisualizationReport.md) on Plotly visualization of haunted places.

---

# DSCI_550_A2

Geospatial and Image Extraction of the Haunted Places Dataset. Assignment 2 for DSCI_550 SP 25. 

Due | 4-4-2025

[Reference](./references/DSCI550_HW_EXTRACT_HAUNTED.pdf)

## Project Organization

Directory Structure the same as A1. Redundant entries eliminated for readability. See astriks and annotations for changes and added scripts. 

```
├── README.md          
|
├── clones             
│
├── clustering         
│
├── data
│   ├── generated_images*   <- haunted places images generated using GenAI
│   ├── processed*          <- The final, canonical data sets for modeling. 
|   │   ├── *features_added_v2.tab | Final dataset with new features
│   
├── notebooks*      <- Added Notebooks 1.09, 1.10, and 5.01 
│
├── pyproject.toml     
│
├── references      <- A2 prompt
│
├── reports             
│   └── figures                 <- Generated graphics and figures to be used in reporting
|   └── referencedPlaces        <- Indices of "Al Capone" and "Keyboard Warrior". Both referenced in final report.
|   └── DSCI 550_A2_Report.docx <- Final report 
│
├── environment.yml    
|
├──  python_3_10.yml    
│                         
│
└── dsci_550_a2*        <- Source code for use in assignment 2.
│   |
|   |── parsingFunctionsv2.py   <- Updated "haunted_places_date" script
|   |── hpimgsDalleAPI.py       <- Generated images 8000-9999
|   |── objectDetection.py      <- Implementation of InceptionV3 Object Detection
|
```

## **Project Overview**

## 1. **Feature Creation**

We added the following columns to our dataset

| Feature              | Method           | Author (Link)                                                   |
|----------------------|------------------|------------------------------------------------------------------|
| GeoTopic_Locations   | GeoTopic Parser  | [rm](notebooks/1.01-dg-haunted_places-audio_features.ipynb)     |
| Named_Entities       | SpACY            | [dg](notebooks/1.09-dg-hpv2-named_entities.ipynb)               |
| GeoTopic_Latitudes   | GeoTopic Parser  | [rm](notebooks/1.01-dg-haunted_places-audio_features.ipynb)     |
| GeoTopic_Longitudes  | GeoTopic Parser  | [rm](notebooks/1.01-dg-haunted_places-audio_features.ipynb)     |
| Image_Pointer        | Pandas lol                | dg                                                                |
| Image_Caption        | Tika Show and Tell                | [ss](notebooks/1.11-ss-hpv2-caption_generation.ipynb)                                                                |
|         | image caption exploration                | [ss](dsci_550_a2/objectDetection.py)                                                                |
| Image_Objects        | Tensorflow                | [km, mm](dsci_550_a2/objectDetection.py)                                                                |

## 5. **Image Generation**

We generated images for indicies 1-9999 using a variety of methods. `Notebooks/5.*` contain image generation code.


| Indicies              | Method           | Author (Link)                                                   |
|----------------------|------------------|------------------------------------------------------------------|
| 1-1999   | Replicate AI  | [ss](notebooks/5.02-ss-hpv2-image_generation.ipynb)     |
| 2000-3999   | Replicate AI  | [rm](notebooks/5.01-rm-hpv2-hpimg_generation_2000_3999.ipynb)     |
| 4000-7999   | Replicate AI  | [ss](notebooks/5.02-ss-hpv2-image_generation.ipynb)     |
| 8000-9999       | DALL·E            | [km](dsci_550_a2/hpimgsDalleAPI.py)               |

## **Report and Summary of Contributions**

Final report is :point_right: [here](reports/TEAM_10_EXTRACT.pdf)



### **Group Contributions :point_down:**

---

**dg**  
- Organized GitHub and wrote `README.md`  
- Extracted named entities using SpaCy  
- Reported findings on named entities in a [supplementary report](./reports/namedEntityRecognitionReport.md)  
- Updated `extract_dates` from [assignment_1](dsci_550_a1/parsingFunctions.py) and wrote updated [`parsingFunctions_v2.py`](dsci_550_a2/parsingFunctions_v2.py) to improve feature coverage  
  - Improved coverage for “haunted_places_date” and “time of day” by 3% and 2% respectively
- Wrote SpaCY findings and thoughts on SpaCY in final report

---

**km**  
- Developed an automated prompting system and utilized OpenAI’s DALL·E to generate custom haunted place images (IDs 8000–9999) based on corresponding descriptions and locations  
- Tested and evaluated Apache Tika’s object detection capabilities using Docker containers  
- Wrote and iterated on Python scripts to adapt and troubleshoot the Tika Docker-based object detection pipeline, addressing architecture compatibility and performance issues  
- Implemented and assessed GPT-4 Vision as a secondary, more accurate solution for object recognition and descriptive captioning  
- Authored the GPT Vision object detection analysis and contributed to the overall object detection methodology section of the final report  

---

**mm**  
- Implemented object detection solution using the InceptionV3 model  
- Wrote a script to map each haunted place’s unique ID to its corresponding AI-generated image and detect the top five objects  
- Managed, organized, and moved the AI-generated haunted images into the correct project directory to match the dataset IDs  
- Wrote script to add a new column, `detected_objects`, to the dataset containing the top five predicted objects for each image  
- Analyzed trends in the detected objects, observing frequent detections of architectural elements  
- Wrote portion of the report about object detection accuracy, trends in detected objects, and the limitations of the models  
- Wrote portion of the report on Tika Docker and InceptionV3 tools and limitations  
- Wrote introduction section of the report outlining the assignment’s objectives, tools used, and methods applied  
- Wrote conclusion section of the report summarizing key insights  

---

**rm**  
- Used the Replicate API to generate images with Stable Diffusion for haunted place IDs 2000–3999 based on the description and apparition type columns  
- Installed the Lucene Geo Gazetteer, built Tika CLI with GeoTopicParser, and created test files to validate the setup  
- Wrote script to extract location names from each row of the haunted places dataset using SpaCy’s Named Entity Recognition and Lucene Geo Gazetteer to retrieve latitude and longitude  
- Successfully started up the Tika server with custom NER model, but was unable to run this on the haunted places dataset due to NaN output errors (GeoTopicParser input parsing issue)  
- Wrote script to count how often each location name appears in the `Locations` column of the dataset  
- Wrote script to find what kinds of entities are most associated with top cities  
- Answered first 2 questions of the report discussing haunted place correlations  

---

**ss**  
- Used the Replicate API to generate images with Stable Diffusion for haunted place IDs 0–1999 and 4000–7999 based on the `description` column  
- Used Tika’s Show and Tell Caption Generator (via the `im2txt-rest-tika` Docker container) to generate image captions for all 9,888 haunted place images  
- Wrote a Python script to extract the highest-confidence caption per image and appended captions to the dataset (`Image_Caption` column in `haunted_places_features_added_v2.tab`)  
- Manually reviewed a random sample of 100 captioned images and categorized each as Accurate, Partially Accurate, or Inaccurate  
- Conducted a word frequency analysis on all 9,888 captions using `CountVectorizer` to find most frequently appearing words  
- Wrote part of report on accuracy and trends with Tika’s Show and Tell Caption Generator  
- Wrote part of report on thoughts and experiences using Tika’s Show and Tell Caption Generator  
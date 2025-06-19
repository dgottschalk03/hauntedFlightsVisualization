# Haunted Flights Visualization
---

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Source code used to prepare Raw data for interactive map. Click the links below to learn more :). 
* :point_right: [website](https://danrobocrop.pythonanywhere.com/)
* :point_right: [sources](/static/sources.md)
* :point_right: [original assignment](/references/DSCI550_HW_BIGDATA_HAUNTED.pdf)
## Project Organization

```
├── README.md           <- The top-level README.
|
├── assets              <- css and fonts
│
├── core                <- callbacks and buttons for dash  
│
├── data
│   ├── keywords.json        <- Keywords used in feature extraction. 
│   ├── airport_df.tab       <- airport data used in plot
│   ├── hp_df.tab            <- route data used in plot
│   ├── route_df.tab         <- haunted places dataset with features added
│   ├── haunted_places.tab   <- original haunted_places dataset
│
├── data_processing     <- Scripts for cleaning dataset haunted places dataset and extracting features
│   ├── feature_extraction.py            <- Main pipeline used to add features haunted_places.tab.
│   ├── data_clean.py                    <- data preprocessing 
│   ├── airport_data_joining.py          <- joining flight and airport features
│   ├── feature_extraction_helpers.py    <- regex and parsers used in pipeline
|
├── plots               <- interactive map
│
├── references          <- Original assignment from DSCI_550
│
├── utils               <- utils for site and quering
|   ├── dataLoader.py           <- loads data for dashboard 
|   ├── flightFunctions.py      <- mathematics for flight trajectories
|   ├── feature_extraction.py   <- optimize data for storage and query   
|   ├── query.py                <- query logic for interactive map

```

---

## **Notes on Methododolgy**

### ✈️ **Airport Radius of Influence**

I filtered out closed airports and determined the radii of influence for the following categories using the [FAA Airspace Guidelines](https://www.faa.gov/sites/faa.gov/files/17_phak_ch15.pdf):

| **Airport Type**                 | **Class** | **Radius of Influence** | **Notes**                                                                                                 |
|----------------------------------|-----------|-------------------------|-----------------------------------------------------------------------------------------------------------|
| **small_airports**               | Class D   | 3 Nautical Miles        | Any airport with a control tower.                                                                         |
| **medium_airport**               | Class C   | 5 Nautical Miles        | "Airports of Moderate Importance."                                                                        |
| **large_airport**                | Class B   | 30 Nautical Miles       | Large commercial airports.                                                                                |
| **heliports**                    | N/A       | 1.5 Nautical Miles      | [Heliport Guidelines](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_150_5390_2D_Heliports.pdf) (Figure 7-1) specify a minimum airspace of 4,000 ft. We assumed areas within 3 miles are within the zone of influence. |
| **balloonports, seaplane_bases** | N/A       | 3 Nautical Miles        | Assumed similar to small airports (total cop out I know).                                                                        |

---

### 🛫 **Route Radius of Influence**

#### 🔍 **Determining Proximity**

- **Angular resolution**: The maximum angle between two objects before they appear as one blurred object.  
    - A human with 20/20 vision: ~1 arcminute.
    - This is:  `(1/60) * (1/60) * (π / 180) = π / 10,800 radians.`

- **Angular size formula**:  `θ = L / d`  
    where:
    - `L = 15 meters (Boeing 747 wingspan)`
    - `θ = π / 10,800`

    Solving for `d`:  
    `d = L / θ = 15 / (π / 10,800) ≈ 51,566 meters.`

- **Horizontal displacement**:  
    Dividing by the average cruising altitude (9,144 meters):  
    `51,566 / 9,144 ≈ 5.6 ≈ 50 Km horizontal visibility.`

**Assumption**: Since haunted places likely don't have ideal viewing conditions, we conservatively reduced the radius of influence to ~10 Km.

---

### 🚦 **Flight High-Traffic Flag**

Flags areas with **high air traffic** density:

| **Possible Values** | **Criteria**                                          |
|---------------------|--------------------------------------------------------|
| `True`              | More than 20 flights intersect the location.          |
| `False`             | 20 or fewer flights intersect the location.           |

---

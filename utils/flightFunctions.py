import math
import numpy as np

# Lat/Lon -> (x,y,z)
def cartesian_convert(lat,lon):
    '''
    Converts latitude and longitude to cartesian coordinates.
    '''
    lat = math.radians(lat)
    lon = math.radians(lon)
    x = math.cos(lat) * math.cos(lon)
    y = math.cos(lat) * math.sin(lon)
    z = math.sin(lat)

    return x, y, z
#  (x,y,z) -> Lat/Lon
def lat_lon_convert(x,y,z):
    '''
    Converts cartesian to latitude and longitude
    '''
    # Phi = angle formed by z and radius of sphere
    lat = math.degrees(math.atan2(z , math.sqrt(x**2 + y**2)))
    # Theta = angle formed by x and y
    lon = math.degrees(math.atan2(y,x))
        

    return lat, lon
# Spherical Linear Interporlation (for flight paths)
def slerp(p1: list[float, float, float], p2: list[float, float, float], t: int) -> list[float, float, float]:
    '''
    spherical linear interpolation in cartesian coordinates.
    Input:
        [p1]    - Point 1 in cartesian coordinates.
        [p2]    - Point 2 in cartesian coordinates.
        [t]     - Value in [0,1]. 
    Returns:
        [pt]    - Point in interpolation in cartesian coordinates
    '''
    ## Unpack Cartesian ##
    x1,y1,z1 = p1 
    x2,y2,z2 = p2

    ## Dot Product ##
    dp = (x1 * x2) + (y1 * y2) + (z1 * z2)

    ## Angle between points ##
    theta = math.acos(dp)
    sin_theta = math.sin(theta)

    ## Interpolation factor ##
    interp1 = math.sin(theta * (1-t)) / sin_theta
    interp2 = math.sin(theta * (t)) / sin_theta

    ## Transform Coordinates ##
    xt = (x1 * interp1) + (x2 * interp2)
    yt = (y1 * interp1) + (y2 * interp2)
    zt = (z1 * interp1) + (z2 * interp2)

    return lat_lon_convert(xt, yt, zt)
# Flight Path Calculator
def flight_trajectory(p1: [float, float], p2: [float, float], n : int) -> list[tuple[float, float]]: 
    '''
    Calculate flight trajectory between two locations.
    Input:
        [p1]    - Point 1. [latitude, longitude]
        [p2]    - Point 2. [latitude, longitude]
        [n]     - number of points
    Returns:
        [path]  - list of points in flight path. [latitude, longitude]
    '''
    ## Initialize Path ##
    path = list()

    ## Unpack Longitude and Latitude ##
    lat1, long1 = p1 
    lat2, long2 = p2

    x1,y1,z1 = cartesian_convert(lat1, long1) 

    xn, yn, zn = cartesian_convert(lat2, long2) 

    for i in range(n+1):
        path.append(slerp([x1,y1,z1], [xn, yn, zn], i / n))

    return path
# Flight Path Intersection Calculator
def flight_trajectory_radius(path: list[tuple[float, float]], d: int) -> list[tuple[float, float]]:
    '''
    Calculate parallel trajectories that are d meters away.
    Input:
        [path]           - flight path. list of (latitude, longitude) coords.
        [d]              - Distance of parallel path
    Returns:
        [path_positive]  - parallel flight path in the positive norm direction
        [path_negative] - parallel flight path in the negative norm direction

    Source:
    https://www.starpath.com/calc/Distance%20Calculators/degree.html 
        Degree of Longitude = 111035 m (Over continental U.S.)
        Degree of Latitude = 85394 m  (Over continental U.S.)
    '''   

    # Parallel Path in Positive Direction
    path_positive = []
    # Parallel Path in Negative Direction
    path_negative = []
    # 1 degree longitude = 111035 [m]
    lon_factor = d / 111035
    # 1 degree latitude = 85494 [m]
    lat_factor = d / 85494

    ## Iterate through points ##
    for i, _ in enumerate(path[:-1]):

        # Unpack current and next coord #
        lat1, lon1 = path[i]
        lat2, lon2 = path[i+1]

        # change in degrees #
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # calculate norm  and norm vectors#
        norm = math.sqrt(dlat**2 + dlon**2)
        if norm == 0:
            continue
        
        norm_vec_lat = - dlon / norm
        norm_vec_lon = dlat  / norm

        # project current coord in positive norm direction. Add to path_positive #
        path_positive.append((lat1 + (norm_vec_lat) * lat_factor ,
                              lon1 + (norm_vec_lon) * lon_factor))
        
        # project current coord in negative norm direction. Add to path_negative#
        path_negative.append((lat1 - (norm_vec_lat) * lat_factor ,
                              lon1 - (norm_vec_lon) * lon_factor))
    ## Add final point ##

    path_positive.append((lat2 + (norm_vec_lat * lat_factor) , lon2 + (norm_vec_lon * lon_factor)))
    path_negative.append((lat2 - (norm_vec_lat * lat_factor) , lon2 - (norm_vec_lon * lon_factor)))

    return path_positive, path_negative
# Check if two (lat, lon) are within d km
def lat_lon_intersect(p1: [float, float], p2: [float, float], d: int) -> bool:
    '''
    Calculates whether two points in degrees longitude and latitude are within a d km of each other.
    Input:
        [p1]    - Point 1. [latitude, longitude]
        [p2]    - Point 2. [latitude, longitude]
        [d]     - Distance in m
    Returns:
        [Bool]  - Wether or not points are within d KM of eachother
    Source:
    https://www.starpath.com/calc/Distance%20Calculators/degree.html 
        Degree of Longitude = 111035 m (Over continental U.S.)
        Degree of Latitude = 85394 m  (Over continental U.S.)

    eg:
    >>> p1 = [34.0699, 118.4438]  # USC #
    >>> p2 = [34.0224, 118.2851]  # UCLA #

    # USC and UCLA are 11.2 miles ~ 18 km away apart #

    >>> print(lat_lon_intersect(p1, p2, 18000))
        False
    >>> print(lat_lon_intersect(p1, p2, 18500))
        True
    '''
    ## Unpack Coordinates
    lat1, lon1  = p1
    lat2, lon2 = p2

    # 1 degree longitude = 111035 [m]
    lon_factor = 111035
    # 1 degree latitude = 85494 [m]
    lat_factor = 85494

    dlon = (lon2 - lon1) 
    dlat = (lat2 - lat1) 

    dist = math.sqrt((dlon * lon_factor)**2 + (dlat * lat_factor)**2)

    return dist < d
# Intersection helper function
def calculate_intersections(row, p2s, ds):
    '''
    Calculate intersections between a single entry and a list of points and coresponding distances. 
    Steps:
    1. iterate t

    Input:
        [row]                - row of a dataframe
        [df_x]               - dataframe of other entries ['airport_df' or 'route_df']

    Returns:
        [intersecting_idxs]  - indicies of the points that intersect with given row

    NOTE: row must have 'Latitude' and 'Longitude' columns. This is bad practice for generalizability, but it works for now.
    
    eg: 
    >>> calculate_intersections(hp_df.loc[1], airport_df)
    []
    '''

    if len(p2s) != len(ds):
        raise ValueError("p2s and ds must be same length")

    intersections = []

    p1 = (row['Latitude'], row['Longitude'])
    
    for j in range(len(p2s)):
        p2 = p2s[j]
        d = ds[j]
        if isinstance(p2, tuple) and lat_lon_intersect(p1,p2, d):
            intersections.append(j)
        elif isinstance(p2, list) and any([lat_lon_intersect(p1, x, d) for x in p2]):
            intersections.append(j)
            
    return intersections
# Add airports used in intersecting flights #
def add_airports_used_in_flights(hp_df, route_df, airport_df):
    '''
    Updates "Intersecting_Airport_Ids" column with airports used in flights specified in "Intersecting_Route_Ids".

    Steps:
        1. Iterate through haunted places
        2. Iterate through routes in "Intersecting_Route_Ids"
        3. Add source and destination airport IATA Codes to list
        4. Add indicies of airports with matching IATA Codes to "Intersecting_Airport_Ids" column.
        5. Remove Duplicates and Sort. 

    Input:
        [hp_df]         - dataframe of haunted places
        [route_df]      - dataframe of routes
        [airport_df]    - dataframe of airports

    Returns:
        [hp_df]         - dataframe of haunted places with updated column
    '''
    # iterate through haunted place ids in intersection data
    for i in hp_df.index():
        intersecting_airports = list(hp_df.at[i, 'Intersecting_Airport_Ids'])
        iata_codes = []

        for route in hp_df.at[i, 'Intersecting_Route_Ids']:
            source_iata, dest_iata = route_df.at[route, "Source_Airport"], route_df.at[route, "Destination_Airport"]
            intersecting_iata_codes.append(source_iata), intersecting_iata_codes.append(dest_iata)

        airports_used_in_flights = airport_df.loc[airport_df['Iata_Code'].isin(intersecting_iata_codes)].index.tolist()
        [intersecting_airports.append(idx) for idx in airports_used_in_flights]

    return hp_df
# Calculate Circular Path
def generate_circle(p1: list[float, float], r : int, n : int =100) -> list[tuple]:
    '''
    Calculate coordinates of circle around a given point.  
    Input:
        [p1]     - Point 1. [latitude, longitude]
        [r]      - Radius in m
        [n]      - number of points
    Returns:
        [circle] - Zipped latitude and longitude coords of circular path
    '''

    ## Unpack coord ##
    lat, lon = p1 

    ## Convert to radians ##
    lat_r = math.radians(lat)
    lon_r = math.radians(lon)

    thetas = np.linspace(0, 2 * math.pi, n)
    earth_radius = 6378137  

    lat_circle = []
    lon_circle = []

    for theta in thetas:
        delta_lat = (r / earth_radius) * math.cos(theta)
        delta_lon = (r / (earth_radius * math.cos(lat_r))) * math.sin(theta)

        lat_circle.append(math.degrees(lat_r + delta_lat))
        lon_circle.append(math.degrees(lon_r + delta_lon))

    return list(zip(lat_circle, lon_circle))


## Imports ##

# Misc Data Handling #
import pandas as pd
from datetime import date 

# Flight Trajectory Functions #
from utils.flightFunctions import *

# Plotly #
import plotly.graph_objects as go
import plotly.express as px
import textwrap

def haunted_place_textbox(row, primary_tag, additional_tags, separator="|", size_arg = None):
    """
    Generate a formatted HTML string for a row based on specified fields.

    Parameters:
    - row: A pandas Series (a single row of a DataFrame).
    - fields: List of fields (column names) to include.
    - bold_fields: List of fields to bold (optional; if None, all fields will be bolded).
    - separator: String separator between lines (default: "<br>").
    - extra_formatting: Optional dictionary {field: custom_format_string}, where
                        custom_format_string can use {value} as placeholder.

    Returns:
    - A formatted HTML string.
    """
    lines = []
    if size_arg:
        lines.append(f"<b>Location</b>: {row['Location']} | <b>{primary_tag.replace('_', ' ').title()}</b>: {row.get(primary_tag, '')} | <b>{size_arg.replace('_', ' ').title()}</b>: {row.get(size_arg, '')}")
    else: 
        lines.append(f"<b>Location</b>: {row['Location']} | <b>{primary_tag.replace('_', ' ').title()}</b>: {row.get(primary_tag, '')}")
    
    if additional_tags != []:
        additional_tag_line = ['<b>Additional Tags:</b>'] + [f"{row.get(tag, '')}" for tag in additional_tags]
        lines.append(f" {separator} ".join(additional_tag_line))

    lines.append(f"<b>Number of Intersecting Flights</b>: {row['Flight_Intersection_Count']} | <b>Number of Nearby Airports</b>: {row['Aerodrome_Count']}<br>")
    lines.append(f"<b>Description</b>: {row['Description']}")


    return "<br>".join(lines)

def airport_textbox(row):
    """
    Generate a formatted HTML string for a row based on specified fields.

    Parameters:
    - row: A pandas Series (a single row of a DataFrame).
    - fields: List of fields (column names) to include.
    - bold_fields: List of fields to bold (optional; if None, all fields will be bolded).
    - separator: String separator between lines (default: "<br>").
    - extra_formatting: Optional dictionary {field: custom_format_string}, where
                        custom_format_string can use {value} as placeholder.

    Returns:
    - A formatted HTML string.
    """
    lines = []
    name, iata, type = row.get('Name', ''), row.get('Iata_Code', ''), row.get("Type", "")
    # description w/o iata code
    if iata == '0' or iata == "":
        lines.append(f"<b>Name</b>: {name}") # | <b>Airport Type</b>: {type}")
    else:
    # description w/ iata code
        lines.append(f"<b>Name</b>: {name} ({iata})") # | <b>Airport Type</b>: {type}")
    
    return "<br>".join(lines)

# Scaling size of haunted place markers
def scale_size(val, mn=5, mx=25):
    if mx == mn:
        return (mn + mx) / 2  
    return mn + (val - mn) * (mx - mn) / (mx - mn)


## Main Visualization Function ##
def hp_interactive_darkmatter(hp_df, route_df, airport_df, legend_arg, size_arg, additional_tags = None, airport_visibility = []):
    # Initialize trace lists
    all_traces = []

    legend_key = list(legend_arg.keys())[0]
    legend_values = [v for v in legend_arg[legend_key]]

    # Color Palette
    plot_colors = {
    "c-1":"#943FC2",
    "c-2":"#0ABF04",
    "c-3":"#F20707",
    "c-4":"#373BF0",
    "c-5":"#F4DB20",
    "c-6":"#3C2D73",
    "c-7":"#730303",
    "c-8":"#4E7317",
    "c-9":"#FF8EFF",
    "c-10":"#44AFF2",
    "c-11":"#8ED943",
    "c-12":"#026873",
    "c-13":"#012840",
    "c-14":"#C2B35B",
    "c-15":"#04D9B2",
    "c-16":"#260401",
    "c-17":"#7E84F2",
    "c-18":"#BF3604",
    "c-19":"#F5B234", 
    "c-20":"#0D0D0D"
    }
        

    ## Haunted Places Trace 

    # Scaling for scatterplot diameters
    mn_scale, mx_scale = hp_df[size_arg].astype(int).min(), hp_df[size_arg].astype(int).max()
    hp_df['Scaled_Size'] = hp_df[size_arg].astype(int).apply(scale_size, mn=mn_scale, mx=mx_scale)
     
    # Iterate through legend values
    for i, val in enumerate(legend_values):
        
        # Filter Dataset
        hp_df_filtered = hp_df.loc[hp_df[f'{legend_key}'].str.contains(val, na=False)].copy()

        # Add Trace
        trace = (go.Scattermap(
            lon = hp_df_filtered['Longitude'],
            lat = hp_df_filtered['Latitude'],
            hoverinfo = 'skip',
            customdata = np.stack([
                                hp_df_filtered.apply(lambda row: haunted_place_textbox(
                                                row,
                                                primary_tag=f"{legend_key}",
                                                additional_tags=additional_tags,
                                                size_arg=size_arg
                                            ), 
                                        axis=1),
                                ], axis = 1
            ),
            hovertemplate = (
                "%{customdata[0]}<br><br>"
            ),
            mode = 'markers',
            showlegend = True, 
            marker = dict(
                size = hp_df_filtered['Scaled_Size'],
                sizemode = 'area',
                sizemin = 3,
                color = plot_colors[f"c-{i+1}"],
                opacity = 0.8
                ),
                name = val.replace("_", " ").title(), 
                visible = True
            )
        )
        all_traces.append(trace)


    ## Flight Path Traces
    if 'routes' in airport_visibility:
        lats_plot, lons_plot = [] , []

        for row in route_df.itertuples(index = False):   

            lats, lons = zip(*row.Flight_Path)
            lats, lons = list(lats), list(lons)

            lats_plot.extend(lats + [None])
            lons_plot.extend(lons + [None])

        # Add trace
        trace = (go.Scattermap(
            lon= lons_plot,
            lat= lats_plot,
            mode='lines',
            line=dict(width=.5, color='red'),
            opacity = 0.1, 
            hoverinfo = 'skip', 
            name = "Flights",
            visible = True
        ))
        all_traces.append(trace)
    
    ## Airport Traces
    airport_types = airport_df['Type'].unique().tolist()

    # Airport Plot Colors
    airport_plot_colors = {
    'heliport' :        "#591D07 ", # Dark Brown
    'seaplane_base': 	"#A62F03", # Dark Orange
    'balloonport' : 	"#F28705",# Light Orange
    'small_airport' :  "#FFB600", # Yellow
    'medium_airport' :	"#F27405", # Bright Orange
    'large_airport':   "#F25C05" # Orange
    }

    # Plot Trace
    if 'airports' in airport_visibility:
        for airport_type in airport_types:
            # Filter by airport type
            airport_df_filtered = airport_df.loc[airport_df['Type'] == airport_type]

            # Airport Marker 
            airport_marker = (go.Scattermap(
            lon = airport_df_filtered['Longitude_Deg'],
            lat = airport_df_filtered['Latitude_Deg'],
            hoverinfo = 'skip',
            customdata = np.stack([
                                airport_df_filtered.apply(airport_textbox, axis=1),
                                ], axis = 1
            ),
            hovertemplate = (
                "%{customdata[0]}<br><br>"
            ),
            mode = 'markers',
            marker = dict(
                size = 2,
                color = airport_plot_colors[airport_type],
                opacity = 0.5
                ),
                name = airport_type.replace('_', ' ').title(),
                visible = True
            ))
            all_traces.append(airport_marker)

            # Airport Radius

            lats_plot, lons_plot = [] , []

            for airport in airport_df_filtered.itertuples():
                
                lats, lons = zip(*airport.Airport_Radius)
                lats, lons = list(lats), list(lons)

                lats_plot.extend(lats + [None])
                lons_plot.extend(lons + [None])
            
            airport_radii = (go.Scattermap(
            lon = lons_plot,
            lat = lats_plot,
            hoverinfo = 'skip',
            mode = 'lines',
            line = dict(
                width = 0.2,
                color = airport_plot_colors[airport_type],
                ),
                showlegend = False,
                visible = True
            ))
            all_traces.append(airport_radii)

    ## Create Plotly figure 
    fig = go.Figure(data = all_traces)

    fig.update_layout(
        title_text = '',
        map_style = 'carto-darkmatter-nolabels',
        showlegend = True,
        clickmode='event+select',
        hovermode = 'closest',
        legend_title_text = legend_key.replace('_', ' '),
        map_center = dict(lat=38, lon = -95),
        map_zoom = 3,
        font=dict(
            family="Mystery Quest, cursive",
            size=12,
            color="white"
        ),
        paper_bgcolor='black',
        uirevision='haunted-map' # preserves zoom betwen updates
    )


    # Return figure
    return fig



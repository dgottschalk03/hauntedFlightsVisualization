import dash_bootstrap_components as dbc
from dash import html, page_container, dcc

from defaultlayouts import globalconstants

def createlayout(
        headercontents=None,
        leftsidebarcontents=None,
        popupcontents=None,
        popuptitle="",
        rightsidebarcontents=None,
        footercontents=None,
        header_height=globalconstants.header_height,       # Must correspond to value set in styles.css
        footer_height = globalconstants.footer_height,      # Ditto
        ):
    contents = [
            html.Div(children=headercontents, className="page-header"),
            html.Div(
                html.Div(
                    children=page_container, 
                    className="page-inner"     # To get the bottom padding right on a narrow screen. 
                ), 
                className="page-body",
                id = "page-body"
            ),
            dcc.Location(id="main-url"),
    ]

    if leftsidebarcontents is not None:
        contents.append(html.Div(
            children=leftsidebarcontents,
            className="page-navbar", 
            id = "sidebar-container"))
        toggle_button = dbc.Button(
                        ">",
                        id="toggle-sidebar-btn",
                        color="primary",
                        size = "sm",
                        className="sidebar-toggle-btn me-2",  
                        n_clicks=0
                    )
        contents.append(toggle_button)
        
    if popupcontents is not None:
        contents.append(dbc.Offcanvas(
                id="page-default-drawer",
                title=popuptitle,
                children=popupcontents,
                style={   # Styling .page-navbar in CSS doesn't seem to work to do this...
                    "top":f"{header_height}px",
                    "bottom":f"{footer_height}px",
                }
            )
        )

    if rightsidebarcontents is not None:
        contents.append(html.Div(children=rightsidebarcontents, className="page-aside"))

    if footercontents is not None:
        contents.append(html.Div(children=footercontents, className="page-footer"))

    layout = dbc.Container(children=contents, fluid=True)
    return layout

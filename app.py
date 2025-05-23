'''
    Dash / Bootstrap boilerplate for a basic responsive multi-page app
    Author David Harris 2024 
    # -- ... originally based on https://github.com/snehilvj/dmc-docs, author Snehil Vijay
'''
from dash import Dash
import dash_bootstrap_components as dbc
from core import corelayout
from defaultlayouts import header, leftsidebar, rightsidebar, footer

from core import callback_close_drawer   # The import defines the callback, no need to reference it
from core import callback_open_drawer
from core import callback_lightswitch
from core import callback_sidebar

app = Dash(
    __name__, 
    use_pages=True,   
    suppress_callback_exceptions=True,
    external_stylesheets=[
                    dbc.themes.DARKLY,
                    "https://use.fontawesome.com/releases/v5.15.4/css/all.css", # github icon
                    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css",
                    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
                    'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css',
    ],
    # Start page in dark mode
    external_scripts=[
        {
            "src": "",
            "content": 'document.documentElement.setAttribute("data-bs-theme", "dark");'
        }
    ]
)

app._favicon = "hpimg_placeholder.png"            
server = app.server                     

app.layout = dbc.Container(corelayout.createlayout(
    headercontents=header.header(),
    leftsidebarcontents= None,
    popupcontents= "",
    popuptitle= None, 
    rightsidebarcontents= None, 
    footercontents=None
))


if __name__ == "__main__":
    app.run(debug=True, dev_tools_hot_reload = True,host='0.0.0.0', port=8050)  
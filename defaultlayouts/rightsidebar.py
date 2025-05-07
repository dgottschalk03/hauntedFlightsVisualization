from dash import html


def aside():
    aside = [
        html.H3("Right SideBar"),
        html.P("This sidebar disappears when screen width is below 1500px"),
        html.H3("Long text to show scrolling")
    ] 
    return aside
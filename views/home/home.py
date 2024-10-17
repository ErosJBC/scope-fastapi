
from dash.html import Div
from dash_bootstrap_components import Container

from views.home.header import header_section, title_section
from views.home.form import form_section
from views.home.button import button_section

def create_layout() -> Div:
    """
    Create the layout of the home page
    :return: Div containing the layout of the home page
    """
    layout = Div([
        Container([
            header_section,
            title_section,
            form_section,
            button_section
        ], className="p-4 mt-4")
    ])
    return layout

# Create the layout
home_layout = create_layout()
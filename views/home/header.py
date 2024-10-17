"""
A component module for header in the components package.
"""
from dash_bootstrap_components import Row, Col, Button, ButtonGroup

from components.logo import Logo
from components.title import Title
from constants.constants import constants


def generate_header_section() -> tuple[Row, Row]:
    """
    Generate the header section of the home page
    :return: The header section of the home page
    :rtype: tuple[Row, Row]
    """
    header = Row([
        Logo(f"assets/img/logo.png")(),
        Col([
            ButtonGroup(
                [
                    Button(
                        "Sell In",
                        id="sell-in-button",
                        n_clicks=0,
                        className="btn btn-primary",
                    ),
                    Button(
                        "Sell Out",
                        id="sell-out-button",
                        n_clicks=0,
                        className="btn btn-secondary",
                    ),
                ],
                vertical=False,
            )
        ], xs=12, sm=12, md=4, className="text-center"),
    ], className="d-flex flex-column flex-md-row justify-content-between align-items-center gy-5 gx-2")

    title = Row([
        Title(
            h_type=title["h_type"],
            text=title["text"],
            **title["args"]
        )() for title in constants.LIST_TITLE
    ], className="d-flex flex-column justify-content-center align-items-center mt-5")

    return header, title

# Create the header section
header_section, title_section = generate_header_section()
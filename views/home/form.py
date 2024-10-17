from dash_bootstrap_components import Col, Row

from constants.constants import constants
from components.select import Select


def generate_form_section() -> Row:
    """
    Generate the form section of the home page
    :return: The form section of the home page
    :rtype: Row
    """
    new_section = Row([
        Col(
            Select(
                label=select["label"],
                dropdown=select["dropdown"]
            )(),
            **select["col"]
        ) for select in constants.LIST_SELECT
    ], className="mt-4")

    return new_section

# Create the form section
form_section = generate_form_section()
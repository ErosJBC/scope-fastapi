from dash_bootstrap_components import Row, Col

from components.button_action import ButtonAction


def generate_button_section() -> Row:
    """
    Generate the button section of the home page
    :return: The button section of the home page
    :rtype: Row
    """
    new_section = Row([
        Col([
            ButtonAction(
                "button",
                "Generar Reporte",
                id="generate-report-button",
                className="btn btn-primary"
            )()
        ], width="auto"),
        Col([
            ButtonAction(
                "link",
                "Descargar Reporte",
                id="download-report-button",
                className="btn btn-secondary",
                download="report.xlsx",
                href="",
                target="_blank"
            )()
        ], width="auto")
    ], className="d-flex justify-content-center align-items-center gy-2 gx-3 mt-4")

    return new_section

# Create the button section
button_section = generate_button_section()
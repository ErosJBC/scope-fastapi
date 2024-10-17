"""
This file contents the constants used in the project.
"""

class Constants:
    LIST_SELECT = [
        {
            "label": {"children": "Nodo", "className": "mb-1 fw-bold text-muted fs-5"},
            "dropdown": {"id": "nodo-dropdown", "value": None},
            "col": {"xs": 12, "sm": 12, "md": 6, "className": "mb-4"}
        },
        {
            "label": {"children": "Tipo de Descuento", "className": "mb-1 fw-bold text-muted fs-5"},
            "dropdown": {"id": "discount-type-dropdown", "value": None},
            "col": {"xs": 12, "sm": 12, "md": 6, "className": "mb-4"}
        },
        {
            "label": {"children": "Año", "className": "mb-1 fw-bold text-muted fs-5"},
            "dropdown": {"id": "year-dropdown", "value": None},
            "col": {"xs": 12, "sm": 12, "md": 6, "className": "mb-4"}
        },
        {
            "label": {"children": "Mes", "className": "mb-1 fw-bold text-muted fs-5"},
            "dropdown": {"id": "month-dropdown", "value": None},
            "col": {"xs": 12, "sm": 12, "md": 6, "className": "mb-4"}
        }
    ]
    LIST_TITLE = [
        {
            "h_type": "h1",
            "text": "SCOPE",
            "args": {
                "style": {
                    "textAlign": "center",
                    "color": "#343a40",
                    "fontWeight": "bold",
                    "marginTop": "10px",
                    "fontSize": "48px",
                },
                "id": "scope-title"
            }
        },
        {
            "h_type": "h5",
            "text": "Settlement Calculation and Optimization Processing Engine",
            "args": {
                "style": {
                    "textAlign": "center",
                    "color": "#6c757d",
                    "fontStyle": "italic",
                    "marginTop": "5px",
                    "marginBottom": "20px",
                    "fontSize": "24px",
                },
                "id": "scope-subtitle"
            }
        }
    ]

# Create an instance of the Constants class
constants = Constants()
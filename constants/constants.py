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
    INPUT_UPDATE= [
        { "component_id": "sell-in-button", "component_property": "n_clicks" },
        { "component_id": "sell-out-button", "component_property": "n_clicks" },
        { "component_id": "nodo-dropdown", "component_property": "value" },
        { "component_id": "year-dropdown", "component_property": "value" },
    ]
    OUTPUT_UDPATE = [
        { "component_id": "nodo-dropdown", "component_property": "options" },
        { "component_id": "discount-type-dropdown", "component_property": "options" },
        { "component_id": "year-dropdown", "component_property": "options" },
        { "component_id": "month-dropdown", "component_property": "options" },
        { "component_id": "sell-in-button", "component_property": "className" },
        { "component_id": "sell-out-button", "component_property": "className" }
    ]
    MONTHS = {
        '1': 'Enero',
        '2': 'Febrero',
        '3': 'Marzo',
        '4': 'Abril',
        '5': 'Mayo',
        '6': 'Junio',
        '7': 'Julio',
        '8': 'Agosto',
        '9': 'Septiembre',
        '10': 'Octubre',
        '11': 'Noviembre',
        '12': 'Diciembre'
    }
    COLUMNS_DATAFRAME = dict_names = {
        'YEAR': 'Año',
        'MONTH': 'Mes',
        'COD_ZENT': 'Responsable de Pago',
        'DES_ZENT': 'Desc Resp.Pago',
        'COD_ZTER': 'Territorio Actual',
        'DES_ZTER': 'Desc Territorio',
        'COD_ZDES': 'Cliente',
        'DES_ZDES': 'Desc Cliente',
        'ETAPA': 'Desc Variedad',
        'FAMILIA': 'Des Familia',
        'COD_PRODUCTO': 'Material',
        'DES_PRODUCTO': 'Desc Material',
        'CLASE_FACTURA': 'Clase de factura',
        'NUM_FACTURA': 'Doc.facturación',
        'REF_FACTURA': 'Referencia',
        'PEDIDO_SAP': 'Pedidos',
        'REF_PEDIDO': 'Referencia clientes',
        'COD_ZDEM': 'Codigo Destinatario',
        'DES_ZDEM': 'Destinatario',
        'SOCIOS': 'Socios',
        'DES_CONDICION_PAGO': 'Condicion de pago',
        'FECHA': 'Fecha factura',
        'CTD_SACOS': 'Cantidad facturada',
        'TMS': 'TM',
        'VALOR_NETO': 'Valor neto',
        'P_BASE': 'P_BASE',
        'D_VOL': 'D_VOL',
        'D_COT': 'D_COT',
        'D_CONT': 'D_CONT',
        'D_LOG': 'D_LOG',
        'R_LOG': 'R_LOG',
        'NCF': 'NCF',
        'P_NETO': 'P_NETO',
        'CONDICION_PAGO': 'Condición de Pago',
        'COD_ZNJE': 'Cod. Nodo',
        'DES_ZNJE': 'Nodo'
    }

# Create an instance of the Constants class
constants = Constants()
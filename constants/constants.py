"""
This file contents the constants used in the project.
"""


class Constants:

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
"""
A module for main in the  package.
"""

import base64
import io
import os
from pathlib import Path
from typing import Any

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, Input, Output, State, dcc, html
from pydantic import FilePath, NonNegativeInt

# TODO: Refactor and modularize code into packages and smaller modules such
#  as callbacks, components, pages, config, data and assets directory, core,
#  utils, etc.
# TODO: Avoid duplicated code by implementing functions and classes for some
#  dependencies
# TODO: Add type annotations for variables, functions arguments and returns
# TODO: Improve the use of integers instead of strings
# TODO: Enhance variables naming with more intuitive and informative names
# TODO: Add docstrings for modules, classes and functions
# TODO: Centralize hard-coded values like dictionaries and lists into some
#  constants or config settings
# Fixme: Validate the use of Dash callbacks to re-instantiate the dataframes

app: Dash = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="S.C.O.P.E.",
    description="SCOPE application developed in Dash framework",
)
dict_names: dict[str, str] = {
    "YEAR": "Año",
    "MONTH": "Mes",
    "COD_ZENT": "Responsable de Pago",
    "DES_ZENT": "Desc Resp.Pago",
    "COD_ZTER": "Territorio Actual",
    "DES_ZTER": "Desc Territorio",
    "COD_ZDES": "Cliente",
    "DES_ZDES": "Desc Cliente",
    "ETAPA": "Desc Variedad",
    "FAMILIA": "Des Familia",
    "COD_PRODUCTO": "Material",
    "DES_PRODUCTO": "Desc Material",
    "CLASE_FACTURA": "Clase de factura",
    "NUM_FACTURA": "Doc.facturación",
    "REF_FACTURA": "Referencia",
    "PEDIDO_SAP": "Pedidos",
    "REF_PEDIDO": "Referencia clientes",
    "COD_ZDEM": "Codigo Destinatario",
    "DES_ZDEM": "Destinatario",
    "SOCIOS": "Socios",
    "DES_CONDICION_PAGO": "Condicion de pago",
    "FECHA": "Fecha factura",
    "CTD_SACOS": "Cantidad facturada",
    "TMS": "TM",
    "VALOR_NETO": "Valor neto",
    "P_BASE": "P_BASE",
    "D_VOL": "D_VOL",
    "D_COT": "D_COT",
    "D_CONT": "D_CONT",
    "D_LOG": "D_LOG",
    "R_LOG": "R_LOG",
    "NCF": "NCF",
    "P_NETO": "P_NETO",
    "CONDICION_PAGO": "Condición de Pago",
    "COD_ZNJE": "Cod. Nodo",
    "DES_ZNJE": "Nodo",
}
dict_month: dict[str, str] = {  # TODO: Replace logic with integers
    "1": "Enero",
    "2": "Febrero",
    "3": "Marzo",
    "4": "Abril",
    "5": "Mayo",
    "6": "Junio",
    "7": "Julio",
    "8": "Agosto",
    "9": "Septiembre",
    "10": "Octubre",
    "11": "Noviembre",
    "12": "Diciembre",
}

# TODO: Use Pydantic FilePath instead
bitacora = "data/Bitacora_ELAX.xlsx"
clientes_SI = "data/Maestra Clientes.xlsx"
reporte_SI = "data/Ventas Maestra Acumulado 2024.xlsx"
reporte_SO = "data/1.2.7. Informe Sell Out.xlsx"
mix_precios = "data/Maestra de Precios.xlsx"


def get_col_widths(dataframe: pd.DataFrame) -> list[int]:
    # Obtener el ancho de las columnas
    widths: list[int] = [
        max([len(str(s)) for s in dataframe[col].values] + [len(col)])
        for col in dataframe.columns
    ]
    return [w + 1 for w in widths]


def col_index_to_letter(
    index: int,
) -> str:
    # Obtener índices para letras de columnas en Excel
    letter: str = ""
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letter = chr(65 + remainder) + letter
    return letter


def encode_image(image_path: FilePath) -> str:
    # Codificar imagen de VTP de interfaz a base64
    with open(image_path, "rb") as image_file:
        encoded_string: str = base64.b64encode(image_file.read()).decode(
            "utf-8"
        )
    return "data:image/jpg;base64," + encoded_string


mcsi: pd.DataFrame = pd.read_excel(clientes_SI)
mcsi = mcsi.loc[
    mcsi["DES_PAIS"].isin(["ECUADOR", "PERÚ"]),
    ["COD_ZNJE", "DES_ZNJE", "COD_ZENT", "COD_ZDES", "COD_ZDEM"],
]
mcsi = mcsi.drop_duplicates().reset_index(drop=True)

bit: pd.DataFrame = pd.read_excel(
    bitacora, sheet_name="ELAX", skiprows=1, dtype=object
)
bit = bit[(bit["Status"] == "Activo") & (bit["Vía"] == "NC")].reset_index(
    drop=True
)
bit = bit[
    [
        "Cliente Tipo",
        "Cod Nodo",
        "Nodo",
        "COD_ZDES",
        "COD_ZDEM ",
        "Tipo de descuento",
        "Tipo Reconocimiento",
        "Aplicación de condición",
        "Tipo",
        "Valor",
        "Condición consumo TM / % SoW",
        "ETAPA",
        "FAMILIA",
        "COD_PRODUCTO",
    ]
]
bit.columns = [
    "SI/SO",
    "COD_ZNJE",
    "DES_ZNJE",
    "COD_ZDES",
    "COD_ZDEM",
    "TIPO_DESCUENTO",
    "PERIODO",
    "APLICACION",
    "TIPO",
    "VALOR",
    "CONDICION",
    "ETAPA",
    "FAMILIA",
    "COD_PRODUCTO",
]

rvn: pd.DataFrame = pd.read_excel(reporte_SI, skiprows=1)
rvn["Periodo"] = rvn["Periodo"].astype(str)
rvn[["Month", "Year"]] = rvn["Periodo"].str.split(".", expand=True)
rvn = rvn[
    [
        "Year",
        "Month",
        "Responsable de Pago",
        "Desc Resp.Pago",
        "Territorio Actual",
        "Desc Territorio",
        "Cliente",
        "Desc Cliente",
        "Desc Variedad",
        "Des Familia",
        "Material",
        "Desc Material",
        "Clase de factura",
        "Doc.facturación",
        "Referencia",
        "Pedidos",
        "Referencia clientes",
        "Codigo Destinatario",
        "Destinatario",
        "Socios",
        "Condicion de pago",
        "Fecha factura",
        "Cantidad facturada",
        "TM",
        "Valor neto",
        "P_BASE",
        "D_VOL",
        "D_COT",
        "D_CONT",
        "D_LOG",
        "R_LOG",
        "NCF",
        "P_NETO",
    ]
]
rvn.columns = [
    "YEAR",
    "MONTH",
    "COD_ZENT",
    "DES_ZENT",
    "COD_ZTER",
    "DES_ZTER",
    "COD_ZDES",
    "DES_ZDES",
    "ETAPA",
    "FAMILIA",
    "COD_PRODUCTO",
    "DES_PRODUCTO",
    "CLASE_FACTURA",
    "NUM_FACTURA",
    "REF_FACTURA",
    "PEDIDO_SAP",
    "REF_PEDIDO",
    "COD_ZDEM",
    "DES_ZDEM",
    "SOCIOS",
    "DES_CONDICION_PAGO",
    "FECHA",
    "CTD_SACOS",
    "TMS",
    "VALOR_NETO",
    "P_BASE",
    "D_VOL",
    "D_COT",
    "D_CONT",
    "D_LOG",
    "R_LOG",
    "NCF",
    "P_NETO",
]
rvn = rvn.merge(
    mcsi[["COD_ZNJE", "DES_ZNJE", "COD_ZENT", "COD_ZDES", "COD_ZDEM"]],
    on=["COD_ZENT", "COD_ZDES", "COD_ZDEM"],
    how="left",
)
rvn = rvn[rvn["COD_ZNJE"].isin(bit["COD_ZNJE"].unique())]
rvn.sort_values(by=["YEAR", "MONTH"], inplace=True)
rvn.reset_index(drop=True, inplace=True)

rvn_so: pd.DataFrame = pd.read_excel(
    reporte_SO, sheet_name="Data", skiprows=1, dtype=object
)
rvn_so = rvn_so[rvn_so["Tipo"] == "Ventas"]
rvn_so["Fecha"] = pd.to_datetime(rvn_so["Fecha"])
rvn_so["MONTH"] = rvn_so["Fecha"].dt.month
rvn_so["YEAR"] = rvn_so["Fecha"].dt.year
rvn_so = rvn_so[
    [
        "MONTH",
        "YEAR",
        "Fecha",
        "Nro_Comprobante",
        "Tip_Condicion_Pago",
        "Cod_Nodo",
        "Distribuidor",
        "COD_ZDES",
        "DES_ZDES",
        "Item Unificado",
        "Descripcion Abreviada",
        "CANTIDAD",
        "Ton",
        "Categoria",
        "Etapa",
    ]
]
rvn_so.columns = [
    "MONTH",
    "YEAR",
    "FECHA",
    "NUM_FACTURA",
    "CONDICION_PAGO",
    "COD_ZNJE",
    "DES_ZNJE",
    "COD_ZDES",
    "DES_ZDES",
    "COD_PRODUCTO",
    "DES_PRODUCTO",
    "CTD_SACOS",
    "TMS",
    "FAMILIA",
    "ETAPA",
]
rvn_so["ETAPA"] = rvn_so["ETAPA"].str.capitalize()
rvn_so = rvn_so[rvn_so["COD_ZNJE"].isin(bit["COD_ZNJE"].unique())]
rvn_so.sort_values(by=["YEAR", "MONTH"], inplace=True)
rvn_so.reset_index(drop=True, inplace=True)

mix: pd.DataFrame = pd.read_excel(
    mix_precios, sheet_name="Salida 29072024", dtype=object
)
mix = mix[
    (mix["Considerar"] == "T") & (mix["Status SKU"] == "ACTIVO")
].reset_index(drop=True)
mix = mix[["Nodo S4", "material", "P. Base", "Total Dscto"]]
mix.columns = ["COD_ZNJE", "COD_PRODUCTO", "PVP", "Dto. Factura"]
mix.drop_duplicates(
    subset=["COD_ZNJE", "COD_PRODUCTO"], keep="last", inplace=True
)
mix["COD_ZNJE"] = mix["COD_ZNJE"].astype(int)
mix["COD_PRODUCTO"] = mix["COD_PRODUCTO"].astype(int)
mix["Dto. Factura"] = mix["Dto. Factura"] / 100

app.layout = html.Div(
    [
        # Contenedor principal para garantizar el centrado y la responsividad
        dbc.Container(
            [
                # Botones 'Sell In' y 'Sell Out' junto con imagen de VTP
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(
                                    src=encode_image(Path("assets/img/logo.png")),
                                    style={
                                        "width": "100%", # Asegura que la imagen se ajuste a la columna
                                        "max-width": "300px", # Imagen máxima de 300px
                                        "display": "block",
                                        "margin-left": "auto",
                                        "margin-right": "auto",
                                    },
                                )
                            ],
                            xs=12, sm=12, md=4, # Ajustes responsivos
                            className="text-center", # Asegura el centrado de la imagen
                        ),
                        dbc.Col(
                            [
                                dbc.ButtonGroup(
                                    [
                                        dbc.Button(
                                            "Sell In",
                                            id="sell-in-button",
                                            n_clicks=0,
                                            className="btn btn-primary",
                                        ),
                                        dbc.Button(
                                            "Sell Out",
                                            id="sell-out-button",
                                            n_clicks=0,
                                            className="btn btn-secondary",
                                        ),
                                    ],
                                    vertical=False,
                                )
                            ],
                            # Ajuste responsivo para diferentes tamaños de pantalla
                            xs=12, sm=12, md=4,
                            className="text-center", # Centrado en pantallas pequeñas
                        ),
                    ],
                    className="d-flex flex-column flex-md-row justify-content-between align-items-center gy-5 gx-2",
                ),
                # Título y subtítulo
                dbc.Row(
                    [
                        html.H1(
                            "SCOPE",
                            style={
                                "textAlign": "center",
                                "color": "#343a40",
                                "fontWeight": "bold",
                                "marginTop": "10px",
                                "fontSize": "48px",
                            },
                        ),
                        html.H5(
                            "Settlement Calculation and Optimization Processing Engine",
                            style={
                                "textAlign": "center",
                                "color": "#6c757d",
                                "fontStyle": "italic",
                                "marginTop": "5px",
                                "marginBottom": "20px",
                                "fontSize": "24px",
                            },
                        ),
                    ],
                    className="d-flex flex-column justify-content-center align-items-center mt-5",
                ),
                # Dropdowns para seleccionar el nodo y tipo de descuento
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Nodo", className="mb-1 fw-bold text-muted fs-5"),
                                dcc.Dropdown(id="nodo-dropdown", value=None),
                            ],
                            xs=12, sm=12, md=6, # Ajustes de ancho según el tamaño de pantalla
                            className="mb-4", # Añadir margen inferior para pantallas pequeñas
                        ),
                        dbc.Col(
                            [
                                html.Label("Tipo de Descuento", className="mb-1 fw-bold text-muted fs-5"),
                                dcc.Dropdown(id="tipo-descuento-dropdown", value=None),
                            ],
                            xs=12, sm=12, md=6,
                            className="mb-4",
                        ),
                        dbc.Col(
                            [
                                html.Label("Año", className="mb-1 fw-bold text-muted fs-5"),
                                dcc.Dropdown(id="year-dropdown", value=None),
                            ],
                            xs=12, sm=12, md=6,
                            className="mb-4",
                        ),
                        dbc.Col(
                            [
                                html.Label("Mes", className="mb-1 fw-bold text-muted fs-5"),
                                dcc.Dropdown(id="month-dropdown", value=None),
                            ],
                            xs=12, sm=12, md=6,
                            className="mb-4",
                        ),
                    ],
                    className="mt-4",
                ),
                # Botones para generar el reporte y descargarlo
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Button(
                                    "Generar Reporte",
                                    id="generate-report-button",
                                    className="btn btn-primary",
                                )
                            ],
                            width="auto",
                        ),
                        dbc.Col(
                            [
                                html.A(
                                    "Descargar Reporte",
                                    id="download-link",
                                    download="reporte.xlsx",
                                    href="",
                                    target="_blank",
                                    className="btn btn-secondary",
                                )
                            ],
                            width="auto",
                        ),
                    ],
                    className="d-flex justify-content-center align-items-center gy-2 gx-3 mt-4",
                ),
            ],
            className="p-4 mt-4", # Añadir padding y margin superior
        )
    ]
)


@app.callback(
    [
        Output("nodo-dropdown", "options"),  # Actualizar las opciones de nodo
        Output("tipo-descuento-dropdown", "options"),
        # Actualizar las opciones de tipo de descuento
        Output("year-dropdown", "options"),  # Actualizar las opciones de año
        Output("month-dropdown", "options"),  # Actualizar las opciones de mes
        Output("sell-in-button", "className"),
        # Actualizar la clase del botón 'Sell In'
        Output("sell-out-button", "className"),
        # Actualizar la clase del botón 'Sell Out'
    ],
    [
        Input("sell-in-button", "n_clicks"),
        # Actualizar el número de clicks del botón 'Sell In'
        Input("sell-out-button", "n_clicks"),
        # Actualizar el número de clicks del botón 'Sell Out'
        Input("nodo-dropdown", "value"),
        # Actualizar el valor seleccionado de nodo
        Input("year-dropdown", "value"),
        # Actualizar el valor seleccionado de año
    ],
)
def update_dropdowns(
    sell_in_clicks: NonNegativeInt,
    sell_out_clicks: NonNegativeInt,
    selected_nodo: str,
    selected_year: NonNegativeInt,  # TODO: Add its NonNegativeInt type hint
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], str, str]:
    # Función para actualizar los dropdowns (elementos interactivos)
    # Determinar cuál botón fue presionado
    if sell_in_clicks < sell_out_clicks:
        selected_liquidacion = "Sell Out"
        sell_in_class = "btn btn-secondary"
        sell_out_class = "btn btn-primary"
    else:
        selected_liquidacion = "Sell In"
        sell_in_class = "btn btn-primary"
        sell_out_class = "btn btn-secondary"

    # Filtrar la bitácora según la liquidación seleccionada y nodos que existan en el maestro de ventas
    filtered_df: pd.DataFrame = bit[
        (bit["SI/SO"] == selected_liquidacion)
        & (bit["COD_ZNJE"].isin(rvn["COD_ZNJE"].unique()))
    ]

    # Filtrar el maestro de ventas con nodos que existan en la bitácora
    rvn_filtered = (
        rvn[rvn["COD_ZNJE"].isin(filtered_df["COD_ZNJE"].unique())]
        if selected_liquidacion == "Sell In"
        else rvn_so[rvn_so["COD_ZNJE"].isin(filtered_df["COD_ZNJE"].unique())]
    )

    # Generar opciones actualizadas para el dropdown de 'Nodo'
    nodo_options: list[dict[str, Any]] = [
        {"label": nodo, "value": nodo}
        for nodo in filtered_df["DES_ZNJE"].unique()
    ]

    # Filtrar bitácora y maestro de ventas según el nodo seleccionado
    if selected_nodo:
        filtered_df = filtered_df[filtered_df["DES_ZNJE"] == selected_nodo]
        rvn_filtered = (
            rvn[
                rvn["COD_ZNJE"]
                == filtered_df[filtered_df["DES_ZNJE"] == selected_nodo][
                    "COD_ZNJE"
                ].unique()[0]
            ]
            if selected_liquidacion == "Sell In"
            else rvn_so[
                rvn_so["COD_ZNJE"]
                == filtered_df[filtered_df["DES_ZNJE"] == selected_nodo][
                    "COD_ZNJE"
                ].unique()[0]
            ]
        )

    # Generar opciones actualizadas para el dropdown de 'Tipo de Descuento'
    tipo_descuento_options: list[dict[str, Any]] = [
        {"label": tipo, "value": tipo}
        for tipo in filtered_df["TIPO_DESCUENTO"].unique()
    ]

    # Generar opciones actualizadas para el dropdown de 'Año'
    year_options: list[dict[str, Any]] = [
        {"label": year, "value": year} for year in rvn_filtered["YEAR"].unique()
    ]

    # Filtrar maestro de ventas según el año seleccionado
    if selected_year:
        rvn_filtered = rvn_filtered[rvn_filtered["YEAR"] == selected_year]

    # Generar opciones actualizadas para el dropdown de 'Mes'
    month_options: list[dict[str, Any]] = [
        {"label": month, "value": month}
        for month in rvn_filtered["MONTH"].unique()
    ]

    # Retornar las opciones actualizadas
    return (
        nodo_options,
        tipo_descuento_options,
        year_options,
        month_options,
        sell_in_class,
        sell_out_class,
    )


@app.callback(
    [
        Output("download-link", "href"),  # Actualizar el enlace de descarga
        Output("download-link", "download"),
        # Actualizar el nombre del archivo de descarga
    ],
    Input("generate-report-button", "n_clicks"),
    # Actualizar el número de clicks del botón 'Generar Reporte'
    [
        State("nodo-dropdown", "value"),
        # Obtener el valor seleccionado de nodo
        State("tipo-descuento-dropdown", "value"),
        # Obtener el valor seleccionado de tipo de descuento
        State("year-dropdown", "value"),  # Obtener el valor seleccionado de año
        State("month-dropdown", "value"),
        # Obtener el valor seleccionado de mes
        Input("sell-in-button", "n_clicks"),
        # Actualizar el número de clicks del botón 'Sell In'
        Input("sell-out-button", "n_clicks"),
        # Actualizar el número de clicks del botón 'Sell Out'
    ],
)
def generate_report(
    n_clicks: NonNegativeInt | None,
    selected_nodo,  # TODO: Add type hints
    selected_tipo,
    selected_year,
    selected_month,
    sell_in_clicks: NonNegativeInt,
    sell_out_clicks: NonNegativeInt,
) -> tuple[str, str]:
    # Crear el callback para generar el archivo de Excel y el enlace de descarga
    if n_clicks is None:
        return (
            "",
            "",
        )  # Si no se ha hecho clic, no generamos el archivo ni el enlace
    # Determinar cuál botón fue presionado
    selected_liquidacion: str = (
        "Sell Out" if sell_in_clicks < sell_out_clicks else "Sell In"
    )

    # Filtrar la bitácora según las selecciones del usuario
    filtered_df = bit[
        (bit["DES_ZNJE"] == selected_nodo)
        & (bit["TIPO_DESCUENTO"] == selected_tipo)
        & (bit["SI/SO"] == selected_liquidacion)
    ]

    # Obtener el período de la bitácora filtrada
    temp = filtered_df["PERIODO"].unique().tolist()[0]
    # Diccionario que mapea los tipos de períodos con sus valores numéricos
    temp_dict: dict[str, int] = {"Mensual": 1, "Bimensual": 2, "Trimestral": 3}

    # Crear una lista de meses en función del período de aplicación
    list_month: list[int | str] = list(range(1, int(selected_month) + 1))[
        -temp_dict[temp] :
    ]
    # Fixme: Update the use of strings to integers instead
    list_month = [
        str(i) for i in list_month
    ]  # Convertir los meses a string para que coincidan con el formato

    # TODO: Avoid the use of global
    global rvn  # Hacer la variable rvn global para poder acceder a ella en la función

    # Filtrar el maestro de ventas según las selecciones del usuario
    filtered_rvn = rvn[
        (rvn["DES_ZNJE"] == selected_nodo)
        & (rvn["YEAR"] == selected_year)
        & (rvn["MONTH"].isin(list_month))
        & (rvn["CLASE_FACTURA"].isin(["ZF01", "ZNC7"]))
    ].reset_index(drop=True)

    # Crear un archivo Excel en memoria
    output: io.BytesIO = (
        io.BytesIO()
    )  # Buffer para guardar el archivo en memoria
    writer: pd.ExcelWriter = pd.ExcelWriter(output, engine="xlsxwriter")
    workbook = writer.book

    # Formato para el encabezado de las columnas
    header_format = workbook.add_format(
        {
            "bold": True,
            "text_wrap": True,
            "valign": "top",
            "fg_color": "#0F243E",  # Color azul oscuro
            "font_color": "#FFFFFF",  # Texto blanco
        }
    )

    # Formato para celdas vacías
    none_format = workbook.add_format(
        {
            "bold": True,
            "text_wrap": True,
            "valign": "top",
            "fg_color": "#FFFFFF",  # Color blanco
            "font_color": "#FFFFFF",
        }
    )

    # Formato para celdas de subtotal
    subtotal_format = workbook.add_format(
        {
            "bold": True,
            "bg_color": "#FFFF00",  # Color amarillo
            "num_format": "#,##0.00",  # Formato numérico con separador de miles
            "border": True,
        }
    )

    # Formato para celdas numéricas
    numeric_format = workbook.add_format(
        {
            "bold": False,
            "bg_color": "#FFFFFF",  # Color amarillo
            "num_format": "#,##0.00",  # Formato numérico con separador de miles
            "border": True,
        }
    )

    # Formato para celdas porcentuales
    percent_format = workbook.add_format(
        {"num_format": "0.00%"}  # Formato porcentual
    )

    # Determinar la aplicación según el valor de 'APLICACION' en el DataFrame filtrado
    aplication = filtered_df["APLICACION"].unique().tolist()[0]
    aplication = (
        "TMS"
        if aplication == "Tonelada"
        else "P_BASE"
        if aplication == "Precio Base"
        else "VALOR_NETO"
    )

    # Columnas para aplicar validaciones
    validadores: list[str] = [
        "COD_ZDES",
        "COD_ZDEM",
        "ETAPA",
        "FAMILIA",
        "COD_PRODUCTO",
    ]

    # Elaborar caso Rebate
    if selected_liquidacion == "Sell In":
        if selected_tipo == "Rebate":
            # Caso específico para 'D. COPACIGULF'
            if selected_nodo == "D. COPACIGULF":
                # Establecer rangos de condiciones de TM
                filtered_df["LOWER_TM"] = (
                    filtered_df["CONDICION"]
                    .str.split(" - ")
                    .str[0]
                    .str.replace("K", "")
                    .astype(float)
                    * 1000
                )
                filtered_df["UPPER_TM"] = (
                    filtered_df["CONDICION"]
                    .str.split(" - ")
                    .str[1]
                    .str.split(" ")
                    .str[0]
                    .str.replace("K", "")
                    .astype(float)
                    * 1000
                )

                # Calcular la media de TM por mes y filtrar según los rangos establecidos
                filtered_df["MEAN_TM"] = float(
                    filtered_rvn[["MONTH", "TMS"]]
                    .groupby(["MONTH"])["TMS"]
                    .sum()
                    .mean()
                )
                filtered_df = filtered_df[
                    (filtered_df["MEAN_TM"] >= filtered_df["LOWER_TM"])
                    & (filtered_df["MEAN_TM"] <= filtered_df["UPPER_TM"])
                ]

                # Extraer el valor de la condición (porcentaje a bonificar)
                valor = filtered_df["VALOR"].unique().tolist()[0]

                # Iterar sobre los meses seleccionados y generar hojas de Excel
                for mes in list_month:
                    sheet_name = "Base {}{}.{}".format(
                        "0" if len(mes) == 1 else "", mes, selected_year
                    )
                    df_export = filtered_rvn.loc[
                        filtered_rvn["MONTH"] == mes
                    ].copy()
                    df_export.drop(
                        [
                            "YEAR",
                            "MONTH",
                            "COD_ZNJE",
                            "DES_ZNJE",
                            "P_BASE",
                            "D_VOL",
                            "D_COT",
                            "D_CONT",
                            "D_LOG",
                            "R_LOG",
                            "NCF",
                            "P_NETO",
                        ],
                        axis=1,
                        inplace=True,
                    )
                    df_export["FECHA"] = pd.to_datetime(
                        df_export["FECHA"]
                    ).dt.strftime("%d/%m/%Y")
                    df_export.rename(columns=dict_names, inplace=True)
                    df_export.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        startrow=2,
                        index=False,
                        header=False,
                    )
                    worksheet = writer.sheets[sheet_name]

                    # Añadir subtotales a las columnas pertinentes
                    for col_num, col_name in enumerate(df_export.columns):
                        col_letter = col_index_to_letter(col_num + 1)
                        if col_name in [
                            "TM",
                            "Valor neto",
                            "Cantidad facturada",
                        ]:
                            formula = f"=SUBTOTAL(9,{col_letter}3:{col_letter}{len(df_export) + 2})"
                            worksheet.write(
                                0, col_num, formula, subtotal_format
                            )
                        else:
                            worksheet.write(0, col_num, "", none_format)

                    # Aplicar formato de encabezados y ajustar anchos de columnas
                    for col_num, (value, width) in enumerate(
                        zip(df_export.columns.values, get_col_widths(df_export))
                    ):
                        worksheet.write(1, col_num, value, header_format)
                        worksheet.set_column(col_num, col_num, width)

                # Agregar hoja de resumen
                sum = (
                    filtered_rvn.groupby("MONTH")
                    .agg({"TMS": "sum", "VALOR_NETO": "sum"})
                    .reset_index()
                )
                sum["MONTH"] = sum["MONTH"].replace(dict_month)

                # Agregar filas adicionales para el resumen
                sum.loc["TOTAL", "MONTH"] = "Promedio VN"
                sum.loc["BASE", "TMS"] = 8000
                sum.loc["BASE", "MONTH"] = "Base"
                sum.loc["EXCEDENTE", "MONTH"] = "Tm excedentes"
                sum.loc["%", "TMS"] = valor * 100
                sum.loc["%", "MONTH"] = "%_Ganado"
                sum.fillna("", inplace=True)
                sum.columns = ["Mes Resumen", "Toneladas", "Dólares"]

                # Añadir hoja de resumen al archivo Excel
                sum.to_excel(writer, sheet_name="Resumen", index=False)
                worksheet = writer.sheets["Resumen"]

                # Obtener el número de filas del resumen actual (sin las filas adicionales)
                n_rows = len(list_month)

                # Añadir fórmulas
                worksheet.write(
                    n_rows + 1,
                    1,
                    f"=SUBTOTAL(1,B2:B{n_rows + 1})",
                    numeric_format,
                )  # Total TMS
                worksheet.write(
                    n_rows + 1,
                    2,
                    f"=SUBTOTAL(1,C2:C{n_rows + 1})",
                    numeric_format,
                )  # Total USD
                worksheet.write(
                    n_rows + 3,
                    1,
                    f"=B{n_rows + 2}-B{n_rows + 3}",
                    numeric_format,
                )  # Excedente
                worksheet.write(
                    n_rows + 5,
                    1,
                    f"=(C{n_rows + 2}/B{n_rows + 2})*B{n_rows + 4}*(B{n_rows + 5}/100)*{len(list_month)}",
                    subtotal_format,
                )  # Bonificación
                worksheet.write(
                    n_rows + 5, 0, "Bonificación", subtotal_format
                )  # Texto Bonificación

                for col_num, value in enumerate(
                    sum.columns.values
                ):  # Formato de encabezados
                    worksheet.write(0, col_num, value, header_format)

                for col_num, width in enumerate(
                    get_col_widths(sum)
                ):  # Ajustar ancho de columnas
                    worksheet.set_column(col_num, col_num, width)

            # Caso rebate para otros nodos distintos de 'D. COPACIGULF'
            else:
                for i, col in enumerate(validadores):
                    expanded = []
                    for _, row in filtered_df.iterrows():
                        if row[col] == "Todo":
                            posibles = filtered_rvn
                            for val_col in validadores[:i]:
                                posibles = posibles[
                                    posibles[val_col] == row[val_col]
                                ]
                            posibles = posibles[col].unique()

                            if len(posibles) > 0:
                                for item in posibles:
                                    new_row = row.copy()
                                    new_row[col] = item
                                    expanded.append(new_row)
                        else:
                            expanded.append(row)

                    filtered_df = pd.DataFrame(expanded)

                # Crear columnas adicionales
                if aplication == "TMS":
                    filtered_rvn = filtered_rvn.merge(
                        filtered_df[
                            [
                                "COD_ZDES",
                                "COD_ZDEM",
                                "ETAPA",
                                "FAMILIA",
                                "COD_PRODUCTO",
                                "VALOR",
                            ]
                        ].drop_duplicates(),
                        how="inner",
                    )
                    filtered_rvn.rename(
                        columns={"VALOR": "Bonificación"}, inplace=True
                    )
                    filtered_rvn["Bonificación"] = pd.to_numeric(
                        filtered_rvn["Bonificación"]
                        .str.replace("$", "")
                        .str.replace(",", "")
                    )
                else:
                    filtered_rvn["PVP"] = (
                        filtered_rvn["P_BASE"] / filtered_rvn["TMS"]
                    )
                    filtered_rvn["Dto. Factura"] = (
                        filtered_rvn["D_VOL"] / filtered_rvn["P_BASE"]
                    )
                    filtered_rvn["P. Crédito"] = filtered_rvn["PVP"] * (
                        1 + filtered_rvn["Dto. Factura"]
                    )
                    filtered_rvn["Dto. Adicional"] = round(
                        (
                            filtered_rvn["P_BASE"]
                            - filtered_rvn["VALOR_NETO"]
                            + filtered_rvn["D_VOL"]
                        )
                        / filtered_rvn["P_BASE"],
                        5,
                    )
                    filtered_rvn = filtered_rvn.merge(
                        filtered_df[
                            [
                                "COD_ZDES",
                                "COD_ZDEM",
                                "ETAPA",
                                "FAMILIA",
                                "COD_PRODUCTO",
                                "VALOR",
                            ]
                        ].drop_duplicates(),
                        how="inner",
                    )
                    filtered_rvn.rename(
                        columns={"VALOR": "Bonificación"}, inplace=True
                    )

                # Calcular 'APORTE' dependiendo de las condiciones
                if aplication == "TMS":
                    filtered_rvn["APORTE"] = (
                        filtered_rvn["TMS"] * filtered_rvn["Bonificación"]
                    )
                elif aplication == "P_BASE":
                    filtered_rvn["APORTE"] = (
                        filtered_rvn["P_BASE"]
                        * filtered_rvn["Bonificación"]
                        * (
                            1
                            + filtered_rvn["D_CONT"]
                            / (filtered_rvn["P_BASE"] + filtered_rvn["D_VOL"])
                        )
                    )
                else:
                    filtered_rvn["APORTE"] = (
                        filtered_rvn["P_BASE"] + filtered_rvn["D_VOL"]
                    ) * filtered_rvn["Bonificación"]  # Revisar con CC

                # Verificar si hay registros para la liquidación
                if filtered_rvn.shape[0] == 0:
                    print(
                        "No se encontraron registros para aplicar la liquidación"
                    )
                else:
                    for mes in list_month:
                        sheet_name = "Base {}{}.{}".format(
                            "0" if len(mes) == 1 else "", mes, selected_year
                        )
                        df_export = filtered_rvn.loc[
                            filtered_rvn["MONTH"] == mes
                        ].copy()
                        df_export.drop(
                            [
                                "YEAR",
                                "MONTH",
                                "CLASE_FACTURA",
                                "SOCIOS",
                                "P_NETO",
                                "P_BASE",
                                "D_VOL",
                                "D_COT",
                                "D_CONT",
                                "D_LOG",
                                "R_LOG",
                                "NCF",
                                "COD_ZNJE",
                                "DES_ZNJE",
                            ],
                            axis=1,
                            inplace=True,
                        )
                        df_export["FECHA"] = pd.to_datetime(
                            df_export["FECHA"]
                        ).dt.strftime("%d/%m/%Y")

                        if aplication != "TMS":
                            # Determinar las posiciones de las columnas en Excel basadas en el DataFrame
                            letter_tm = col_index_to_letter(
                                df_export.columns.get_loc("TMS") + 1
                            )
                            letter_p_base = col_index_to_letter(
                                df_export.columns.get_loc("PVP") + 1
                            )
                            letter_valor = col_index_to_letter(
                                df_export.columns.get_loc("Bonificación") + 1
                            )
                            letter_d_vol = col_index_to_letter(
                                df_export.columns.get_loc("Dto. Factura") + 1
                            )
                            letter_d_adic = col_index_to_letter(
                                df_export.columns.get_loc("Dto. Adicional") + 1
                            )

                        col_aporte = df_export.shape[
                            1
                        ]  # La nueva columna 'APORTE' estará después de la última columna

                        df_export.rename(columns=dict_names, inplace=True)
                        df_export.to_excel(
                            writer,
                            sheet_name=sheet_name,
                            startrow=2,
                            index=False,
                            header=False,
                        )
                        worksheet = writer.sheets[sheet_name]

                        # Escribir la fórmula en Excel para la columna APORTE
                        if aplication == "TMS":
                            for row in range(
                                3, len(df_export) + 2
                            ):  # Suponiendo que los datos comienzan en la fila 2
                                formula = (
                                    f"={letter_tm}{row}*{letter_valor}{row}"
                                )
                                worksheet.write_formula(
                                    f"{col_index_to_letter(col_aporte)}{row}",
                                    formula,
                                )
                        elif aplication == "P_BASE":
                            for row in range(
                                3, len(df_export) + 2
                            ):  # Suponiendo que los datos comienzan en la fila 2
                                formula = f"={letter_tm}{row}*{letter_p_base}{row}*{letter_valor}{row}*(1+{letter_d_adic}{row})"
                                worksheet.write_formula(
                                    f"{col_index_to_letter(col_aporte)}{row}",
                                    formula,
                                )
                        else:
                            for row in range(
                                3, len(df_export) + 2
                            ):  # Suponiendo que los datos comienzan en la fila 2
                                formula = f"={letter_tm}{row}*{letter_p_base}{row}*{letter_valor}{row}*(1+{letter_d_vol}{row}+{letter_d_adic}{row})"
                                worksheet.write_formula(
                                    f"{col_index_to_letter(col_aporte)}{row}",
                                    formula,
                                )

                        # Añadir subtotales a las columnas pertinentes
                        for col_num, col_name in enumerate(df_export.columns):
                            col_letter = col_index_to_letter(col_num + 1)
                            if col_name in [
                                "TM",
                                "Valor neto",
                                "Cantidad facturada",
                                "APORTE",
                            ]:
                                formula = f"=SUBTOTAL(9, {col_letter}3:{col_letter}{len(df_export) + 2})"
                                worksheet.write(
                                    0, col_num, formula, subtotal_format
                                )
                            else:
                                worksheet.write(0, col_num, "", none_format)

                        # Aplicar formato de encabezados y ajustar anchos de columnas
                        for col_num, (value, width) in enumerate(
                            zip(
                                df_export.columns.values,
                                get_col_widths(df_export),
                            )
                        ):  # Formato de encabezados
                            worksheet.write(1, col_num, value, header_format)
                            worksheet.set_column(col_num, col_num, width)

                        worksheet.write(
                            1, col_aporte - 1, "Importe NC", subtotal_format
                        )

                        # Aplicar formato de porcentaje a 'Dto. Factura'
                        col_idx = df_export.columns.get_loc("Dto. Factura")
                        worksheet.set_column(
                            col_idx, col_idx, 18, percent_format
                        )

                        # Aplicar formato de porcentaje a 'Dto. Adicional'
                        col_idx = df_export.columns.get_loc("Dto. Adicional")
                        worksheet.set_column(
                            col_idx, col_idx, 18, percent_format
                        )

                        if aplication != "TMS":
                            # Aplicar formato de porcentaje a 'Bonificación'
                            col_idx = df_export.columns.get_loc("Bonificación")
                            worksheet.set_column(
                                col_idx, col_idx, 18, percent_format
                            )

                    # Agregar hoja de resumen
                    sum = (
                        filtered_rvn.groupby("MONTH")
                        .agg(
                            {"TMS": "sum", "VALOR_NETO": "sum", "APORTE": "sum"}
                        )
                        .reset_index()
                    )
                    sum["MONTH"] = sum["MONTH"].replace(dict_month)

                    # Agregar filas adicionales para el resumen
                    sum.columns = [
                        "Mes Resumen",
                        "Toneladas",
                        "Dólares",
                        "Importe NC",
                    ]
                    sum.loc["TOTAL", "Toneladas"] = sum["Toneladas"].sum()
                    sum.loc["TOTAL", "Dólares"] = sum["Dólares"].sum()
                    sum.loc["TOTAL", "Importe NC"] = sum["Importe NC"].sum()
                    sum.loc["TOTAL", "Mes Resumen"] = "Total"

                    # Añadir hoja de resumen al archivo Excel
                    sum.to_excel(writer, sheet_name="Resumen", index=False)
                    worksheet = writer.sheets["Resumen"]

                    for col_num, value in enumerate(
                        sum.columns.values
                    ):  # Formato de encabezados
                        worksheet.write(0, col_num, value, header_format)

                    for col_num, value in enumerate(
                        sum.iloc[-1]
                    ):  # Formato de subtotales
                        worksheet.write(
                            len(sum), col_num, value, subtotal_format
                        )

                    for col_num, width in enumerate(
                        get_col_widths(sum)
                    ):  # Ajustar ancho de columnas
                        worksheet.set_column(col_num, col_num, width)

            # SO aplicaría por ZDES (No se requiere actualmente)

        elif selected_tipo == "Logístico CR":
            for i, col in enumerate(validadores):
                expanded = []
                for _, row in filtered_df.iterrows():
                    if row[col] == "Todo":
                        posibles = filtered_rvn
                        for val_col in validadores[:i]:
                            posibles = posibles[
                                posibles[val_col] == row[val_col]
                            ]
                        posibles = posibles[col].unique()

                        if len(posibles) > 0:
                            for item in posibles:
                                new_row = row.copy()
                                new_row[col] = item
                                expanded.append(new_row)
                    else:
                        expanded.append(row)

                filtered_df = pd.DataFrame(expanded)

            filtered_rvn = filtered_rvn[
                filtered_rvn["REF_PEDIDO"].str.contains("RECOGE")
            ].reset_index(drop=True)
            filtered_rvn = filtered_rvn.merge(
                filtered_df[
                    [
                        "COD_ZDES",
                        "COD_ZDEM",
                        "ETAPA",
                        "FAMILIA",
                        "COD_PRODUCTO",
                        "VALOR",
                    ]
                ].drop_duplicates(),
                how="inner",
            )
            filtered_rvn["VALOR"] = pd.to_numeric(
                filtered_rvn["VALOR"].str.replace("$", "").str.replace(",", "")
            )
            filtered_rvn.rename(columns={"VALOR": "Bonificación"}, inplace=True)
            filtered_rvn["APORTE"] = filtered_rvn["TMS"] * filtered_rvn[
                "Bonificación"
            ].astype(float)

            if filtered_rvn.shape[0] == 0:
                print("No se encontraron registros en el mes seleccionado.")
            else:
                sheet_name = "Base {}{}.{}".format(
                    "0" if len(selected_month) == 1 else "",
                    selected_month,
                    selected_year,
                )
                df_export = filtered_rvn.loc[
                    filtered_rvn["MONTH"] == selected_month
                ].copy()
                df_export.drop(
                    [
                        "YEAR",
                        "MONTH",
                        "CLASE_FACTURA",
                        "SOCIOS",
                        "P_NETO",
                        "P_BASE",
                        "D_VOL",
                        "D_COT",
                        "D_CONT",
                        "D_LOG",
                        "R_LOG",
                        "NCF",
                        "COD_ZNJE",
                        "DES_ZNJE",
                    ],
                    axis=1,
                    inplace=True,
                )
                df_export["FECHA"] = pd.to_datetime(
                    df_export["FECHA"]
                ).dt.strftime("%d/%m/%Y")

                # Determinar las posiciones de las columnas en Excel basadas en el DataFrame
                col_tm = df_export.columns.get_loc("TMS")
                col_valor = df_export.columns.get_loc("Bonificación")
                col_aporte = df_export.shape[
                    1
                ]  # La nueva columna 'APORTE' estará después de la última columna

                # Convertir los índices de columna a las letras correspondientes en Excel
                letter_tm = col_index_to_letter(col_tm + 1)
                letter_valor = col_index_to_letter(col_valor + 1)

                df_export.rename(columns=dict_names, inplace=True)
                df_export.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    startrow=2,
                    index=False,
                    header=False,
                )
                worksheet = writer.sheets[sheet_name]

                for row in range(
                    3, len(df_export) + 2
                ):  # Suponiendo que los datos comienzan en la fila 2
                    formula = f"={letter_tm}{row}*{letter_valor}{row}"
                    worksheet.write_formula(
                        f"{col_index_to_letter(col_aporte)}{row}", formula
                    )

                for col_num, col_name in enumerate(
                    df_export.columns
                ):  # Añadir subtotales
                    col_letter = col_index_to_letter(col_num + 1)
                    if col_name in [
                        "TM",
                        "Valor neto",
                        "Cantidad facturada",
                        "APORTE",
                    ]:
                        formula = f"=SUBTOTAL(9, {col_letter}3:{col_letter}{len(df_export) + 2})"
                        worksheet.write(0, col_num, formula, subtotal_format)
                    else:
                        worksheet.write(0, col_num, "", none_format)

                for col_num, (value, width) in enumerate(
                    zip(df_export.columns.values, get_col_widths(df_export))
                ):  # Formato de encabezados
                    worksheet.write(1, col_num, value, header_format)
                    worksheet.set_column(col_num, col_num, width)

                worksheet.write(
                    1, col_aporte - 1, "Importe NC", subtotal_format
                )

                # Agregar hoja de resumen
                sum = (
                    filtered_rvn.groupby("DES_ZDEM")
                    .agg({"TMS": "sum", "VALOR_NETO": "sum", "APORTE": "sum"})
                    .reset_index()
                )
                sum.columns = ["DESTINATARIO", "TMS", "USD", "APORTE"]
                sum.loc["TOTAL", "TMS"] = sum["TMS"].sum()
                sum.loc["TOTAL", "USD"] = sum["USD"].sum()
                sum.loc["TOTAL", "APORTE"] = sum["APORTE"].sum()
                sum.loc["TOTAL", "DESTINATARIO"] = "Total"
                sum.to_excel(writer, sheet_name="Resumen", index=False)
                worksheet = writer.sheets["Resumen"]

                for col_num, value in enumerate(
                    sum.columns.values
                ):  # Formato de encabezados
                    worksheet.write(0, col_num, value, header_format)

                for col_num, value in enumerate(
                    sum.iloc[-1]
                ):  # Formato de subtotales
                    worksheet.write(
                        len(sum), col_num, value, subtotal_format
                    )  # Ajusta aquí si necesitas escribir un valor diferente o una fórmula

                for col_num, width in enumerate(
                    get_col_widths(sum)
                ):  # Ajustar ancho de columnas
                    worksheet.set_column(col_num, col_num, width)

            # Es fijo mensual $xTM, no aplica SO.

        elif selected_tipo == "Logístico Fluvial":
            for i, col in enumerate(validadores):
                expanded = []
                for _, row in filtered_df.iterrows():
                    if row[col] == "Todo":
                        posibles = filtered_rvn
                        for val_col in validadores[:i]:
                            posibles = posibles[
                                posibles[val_col] == row[val_col]
                            ]
                        posibles = posibles[col].unique()

                        if len(posibles) > 0:
                            for item in posibles:
                                new_row = row.copy()
                                new_row[col] = item
                                expanded.append(new_row)
                    else:
                        expanded.append(row)

                filtered_df = pd.DataFrame(expanded)

            filtered_rvn = filtered_rvn.merge(
                filtered_df[
                    [
                        "COD_ZDES",
                        "COD_ZDEM",
                        "ETAPA",
                        "FAMILIA",
                        "COD_PRODUCTO",
                        "VALOR",
                    ]
                ].drop_duplicates(),
                how="inner",
            )
            filtered_rvn["VALOR"] = pd.to_numeric(
                filtered_rvn["VALOR"].str.replace("$", "").str.replace(",", "")
            )
            filtered_rvn.rename(columns={"VALOR": "Bonificación"}, inplace=True)
            filtered_rvn["APORTE"] = filtered_rvn["TMS"] * filtered_rvn[
                "Bonificación"
            ].astype(float)

            if filtered_rvn.shape[0] == 0:
                print("No se encontraron registros en el mes seleccionado.")
            else:
                sheet_name = "Base {}{}.{}".format(
                    "0" if len(selected_month) == 1 else "",
                    selected_month,
                    selected_year,
                )
                df_export = filtered_rvn.loc[
                    filtered_rvn["MONTH"] == selected_month
                ].copy()
                df_export.drop(
                    [
                        "YEAR",
                        "MONTH",
                        "CLASE_FACTURA",
                        "SOCIOS",
                        "P_NETO",
                        "P_BASE",
                        "D_VOL",
                        "D_COT",
                        "D_CONT",
                        "D_LOG",
                        "R_LOG",
                        "NCF",
                        "COD_ZNJE",
                        "DES_ZNJE",
                    ],
                    axis=1,
                    inplace=True,
                )
                df_export["FECHA"] = pd.to_datetime(
                    df_export["FECHA"]
                ).dt.strftime("%d/%m/%Y")

                # Determinar las posiciones de las columnas en Excel basadas en el DataFrame
                col_tm = df_export.columns.get_loc("TMS")
                col_valor = df_export.columns.get_loc("Bonificación")
                col_aporte = df_export.shape[
                    1
                ]  # La nueva columna 'APORTE' estará después de la última columna

                # Convertir los índices de columna a las letras correspondientes en Excel
                letter_tm = col_index_to_letter(col_tm + 1)
                letter_valor = col_index_to_letter(col_valor + 1)

                df_export.rename(columns=dict_names, inplace=True)
                df_export.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    startrow=2,
                    index=False,
                    header=False,
                )
                worksheet = writer.sheets[sheet_name]

                for row in range(
                    3, len(df_export) + 2
                ):  # Suponiendo que los datos comienzan en la fila 2
                    formula = f"={letter_tm}{row}*{letter_valor}{row}"
                    worksheet.write_formula(
                        f"{col_index_to_letter(col_aporte)}{row}", formula
                    )

                for col_num, col_name in enumerate(
                    df_export.columns
                ):  # Añadir subtotales
                    col_letter = col_index_to_letter(col_num + 1)
                    if col_name in [
                        "TM",
                        "Valor neto",
                        "Cantidad facturada",
                        "APORTE",
                    ]:
                        formula = f"=SUBTOTAL(9, {col_letter}3:{col_letter}{len(df_export) + 2})"
                        worksheet.write(0, col_num, formula, subtotal_format)
                    else:
                        worksheet.write(0, col_num, "", none_format)

                for col_num, (value, width) in enumerate(
                    zip(df_export.columns.values, get_col_widths(df_export))
                ):  # Formato de encabezados
                    worksheet.write(1, col_num, value, header_format)
                    worksheet.set_column(col_num, col_num, width)

                worksheet.write(
                    1, col_aporte - 1, "Importe NC", subtotal_format
                )

                # Agregar hoja de resumen
                sum = (
                    filtered_rvn.groupby("DES_ZDEM")
                    .agg({"TMS": "sum", "VALOR_NETO": "sum", "APORTE": "sum"})
                    .reset_index()
                )
                sum.columns = ["DESTINATARIO", "TMS", "USD", "APORTE"]
                sum.loc["TOTAL", "TMS"] = sum["TMS"].sum()
                sum.loc["TOTAL", "USD"] = sum["USD"].sum()
                sum.loc["TOTAL", "APORTE"] = sum["APORTE"].sum()
                sum.loc["TOTAL", "DESTINATARIO"] = "Total"
                sum.to_excel(writer, sheet_name="Resumen", index=False)
                worksheet = writer.sheets["Resumen"]

                for col_num, value in enumerate(
                    sum.columns.values
                ):  # Formato de encabezados
                    worksheet.write(0, col_num, value, header_format)

                for col_num, value in enumerate(
                    sum.iloc[-1]
                ):  # Formato de subtotales
                    worksheet.write(
                        len(sum), col_num, value, subtotal_format
                    )  # Ajusta aquí si necesitas escribir un valor diferente o una fórmula

                for col_num, width in enumerate(
                    get_col_widths(sum)
                ):  # Ajustar ancho de columnas
                    worksheet.set_column(col_num, col_num, width)

            # No aplica SO.

        elif (
            selected_tipo == "Reconocimiento Comercial"
        ):  # Todo es porcentual por sku
            for i, col in enumerate(validadores):
                expanded = []
                for _, row in filtered_df.iterrows():
                    if row[col] == "Todo":
                        posibles = filtered_rvn
                        for val_col in validadores[:i]:
                            posibles = posibles[
                                posibles[val_col] == row[val_col]
                            ]
                        posibles = posibles[col].unique()

                        if len(posibles) > 0:
                            for item in posibles:
                                new_row = row.copy()
                                new_row[col] = item
                                expanded.append(new_row)
                    else:
                        expanded.append(row)

                filtered_df = pd.DataFrame(expanded)

            if aplication == "TMS":
                filtered_rvn = filtered_rvn.merge(
                    filtered_df[
                        [
                            "COD_ZDES",
                            "COD_ZDEM",
                            "ETAPA",
                            "FAMILIA",
                            "COD_PRODUCTO",
                            "VALOR",
                        ]
                    ].drop_duplicates(),
                    how="inner",
                )
                filtered_rvn.rename(
                    columns={"VALOR": "Bonificación"}, inplace=True
                )
                filtered_rvn["Bonificación"] = pd.to_numeric(
                    filtered_rvn["Bonificación"]
                    .str.replace("$", "")
                    .str.replace(",", "")
                )
            else:
                filtered_rvn["PVP"] = (
                    filtered_rvn["P_BASE"] / filtered_rvn["TMS"]
                )
                filtered_rvn["Dto. Factura"] = (
                    filtered_rvn["D_VOL"] / filtered_rvn["P_BASE"]
                )
                filtered_rvn["P. Crédito"] = filtered_rvn["PVP"] * (
                    1 + filtered_rvn["Dto. Factura"]
                )
                filtered_rvn["Dto. Adicional"] = round(
                    (
                        filtered_rvn["P_BASE"]
                        - filtered_rvn["VALOR_NETO"]
                        + filtered_rvn["D_VOL"]
                    )
                    / filtered_rvn["P_BASE"],
                    5,
                )
                filtered_rvn = filtered_rvn.merge(
                    filtered_df[
                        [
                            "COD_ZDES",
                            "COD_ZDEM",
                            "ETAPA",
                            "FAMILIA",
                            "COD_PRODUCTO",
                            "VALOR",
                        ]
                    ].drop_duplicates(),
                    how="inner",
                )
                filtered_rvn.rename(
                    columns={"VALOR": "Bonificación"}, inplace=True
                )

            # Calcular 'APORTE' dependiendo de las condiciones
            if aplication == "TMS":
                filtered_rvn["APORTE"] = (
                    filtered_rvn["TMS"] * filtered_rvn["Bonificación"]
                )
            elif aplication == "P_BASE":
                filtered_rvn["APORTE"] = (
                    filtered_rvn["P_BASE"]
                    * filtered_rvn["Bonificación"]
                    * (
                        1
                        + filtered_rvn["D_CONT"]
                        / (filtered_rvn["P_BASE"] + filtered_rvn["D_VOL"])
                    )
                )
            else:
                filtered_rvn["APORTE"] = (
                    filtered_rvn["P_BASE"] + filtered_rvn["D_VOL"]
                ) * filtered_rvn["Bonificación"]  # Revisar con CC

            # Verificar si hay registros para la liquidación
            if filtered_rvn.shape[0] == 0:
                print("No se encontraron registros para aplicar la liquidación")
            else:
                for mes in list_month:
                    sheet_name = "Base {}{}.{}".format(
                        "0" if len(mes) == 1 else "", mes, selected_year
                    )
                    df_export = filtered_rvn.loc[
                        filtered_rvn["MONTH"] == mes
                    ].copy()
                    df_export.drop(
                        [
                            "YEAR",
                            "MONTH",
                            "CLASE_FACTURA",
                            "SOCIOS",
                            "P_NETO",
                            "P_BASE",
                            "D_VOL",
                            "D_COT",
                            "D_CONT",
                            "D_LOG",
                            "R_LOG",
                            "NCF",
                            "COD_ZNJE",
                            "DES_ZNJE",
                        ],
                        axis=1,
                        inplace=True,
                    )
                    df_export["FECHA"] = pd.to_datetime(
                        df_export["FECHA"]
                    ).dt.strftime("%d/%m/%Y")

                    if aplication != "TMS":
                        # Determinar las posiciones de las columnas en Excel basadas en el DataFrame
                        letter_tm = col_index_to_letter(
                            df_export.columns.get_loc("TMS") + 1
                        )
                        letter_p_base = col_index_to_letter(
                            df_export.columns.get_loc("PVP") + 1
                        )
                        letter_valor = col_index_to_letter(
                            df_export.columns.get_loc("Bonificación") + 1
                        )
                        letter_d_vol = col_index_to_letter(
                            df_export.columns.get_loc("Dto. Factura") + 1
                        )
                        letter_d_adic = col_index_to_letter(
                            df_export.columns.get_loc("Dto. Adicional") + 1
                        )

                    col_aporte = df_export.shape[
                        1
                    ]  # La nueva columna 'APORTE' estará después de la última columna

                    df_export.rename(columns=dict_names, inplace=True)
                    df_export.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        startrow=2,
                        index=False,
                        header=False,
                    )
                    worksheet = writer.sheets[sheet_name]

                    # Escribir la fórmula en Excel para la columna APORTE
                    if aplication == "TMS":
                        for row in range(
                            3, len(df_export) + 2
                        ):  # Suponiendo que los datos comienzan en la fila 2
                            formula = f"={letter_tm}{row}*{letter_valor}{row}"
                            worksheet.write_formula(
                                f"{col_index_to_letter(col_aporte)}{row}",
                                formula,
                            )
                    elif aplication == "P_BASE":
                        for row in range(
                            3, len(df_export) + 2
                        ):  # Suponiendo que los datos comienzan en la fila 2
                            formula = f"={letter_tm}{row}*{letter_p_base}{row}*{letter_valor}{row}*(1+{letter_d_adic}{row})"
                            worksheet.write_formula(
                                f"{col_index_to_letter(col_aporte)}{row}",
                                formula,
                            )
                    else:
                        for row in range(
                            3, len(df_export) + 2
                        ):  # Suponiendo que los datos comienzan en la fila 2
                            formula = f"={letter_tm}{row}*{letter_p_base}{row}*{letter_valor}{row}*(1+{letter_d_vol}{row}+{letter_d_adic}{row})"
                            worksheet.write_formula(
                                f"{col_index_to_letter(col_aporte)}{row}",
                                formula,
                            )

                    # Añadir subtotales a las columnas pertinentes
                    for col_num, col_name in enumerate(
                        df_export.columns
                    ):  # Añadir subtotales
                        col_letter = col_index_to_letter(col_num + 1)
                        if col_name in [
                            "TM",
                            "Valor neto",
                            "Cantidad facturada",
                            "APORTE",
                        ]:
                            formula = f"=SUBTOTAL(9, {col_letter}3:{col_letter}{len(df_export) + 2})"
                            worksheet.write(
                                0, col_num, formula, subtotal_format
                            )
                        else:
                            worksheet.write(0, col_num, "", none_format)

                    # Aplicar formato de encabezados y ajustar anchos de columnas
                    for col_num, (value, width) in enumerate(
                        zip(df_export.columns.values, get_col_widths(df_export))
                    ):  # Formato de encabezados
                        worksheet.write(1, col_num, value, header_format)
                        worksheet.set_column(col_num, col_num, width)

                # Agregar hoja de resumen
                sum = (
                    filtered_rvn.groupby(["MONTH", "DES_ZDEM"])
                    .agg({"TMS": "sum", "VALOR_NETO": "sum", "APORTE": "sum"})
                    .reset_index()
                )
                sum["MONTH"] = sum["MONTH"].replace(dict_month)
                sum.columns = ["CLIENTE", "MES", "TMS", "USD", "APORTE"]
                sum.loc["TOTAL", "TMS"] = sum["TMS"].sum()
                sum.loc["TOTAL", "USD"] = sum["USD"].sum()
                sum.loc["TOTAL", "APORTE"] = sum["APORTE"].sum()
                sum.loc["TOTAL", "MES"] = "Total"
                sum.fillna("", inplace=True)
                sum.to_excel(writer, sheet_name="Resumen", index=False)
                worksheet = writer.sheets["Resumen"]

                for col_num, value in enumerate(
                    sum.columns.values
                ):  # Formato de encabezados
                    worksheet.write(0, col_num, value, header_format)

                for col_num, value in enumerate(
                    sum.iloc[-1]
                ):  # Formato de subtotales
                    worksheet.write(len(sum), col_num, value, subtotal_format)

                for col_num, width in enumerate(
                    get_col_widths(sum)
                ):  # Ajustar ancho de columnas
                    worksheet.set_column(col_num, col_num, width)
        else:
            print("Tipo de descuento no reconocido")

            df_export = filtered_rvn.copy()
            df_export.to_excel(
                writer,
                sheet_name="Reporte",
                startrow=1,
                index=False,
                header=False,
            )
            worksheet = writer.sheets["Reporte"]

            for col_num, col_name in enumerate(
                df_export.columns
            ):  # Añadir subtotales
                col_letter = col_index_to_letter(col_num + 1)
                if col_name in ["TMS", "VALOR_NETO", "CTD_SACOS"]:
                    formula = f"=SUBTOTAL(9, {col_letter}3:{col_letter}{len(df_export) + 2})"
                    worksheet.write(0, col_num, formula, subtotal_format)
                else:
                    worksheet.write(0, col_num, "", none_format)

            for col_num, (value, width) in enumerate(
                zip(df_export.columns.values, get_col_widths(df_export))
            ):  # Formato de encabezados
                worksheet.write(1, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, width)

    else:
        # Homologar formato de Familia a Info_SellOut
        filtered_df["FAMILIA"] = (
            filtered_df["FAMILIA"].str.split(" ").str[1].str[:3].str.upper()
        )

        global rvn_so

        filtered_rvn = (
            rvn_so[
                (
                    rvn_so["COD_ZNJE"]
                    == filtered_df[filtered_df["DES_ZNJE"] == selected_nodo][
                        "COD_ZNJE"
                    ]
                    .unique()
                    .tolist()[0]
                )
                & (rvn_so["YEAR"] == int(selected_year))
                & (rvn_so["MONTH"].isin([int(i) for i in list_month]))
            ]
            .reset_index(drop=True)
            .copy()
        )

        filtered_rvn["COD_ZDES"] = filtered_rvn["COD_ZDES"].astype(int)

        validadores = [
            "COD_ZDES",
            "ETAPA",
            "FAMILIA",
            "COD_PRODUCTO",
        ]  # ZDEM siempre es todo, Informe SO no tiene ZDEM compatible

        for i, col in enumerate(validadores):
            expanded = []
            for _, row in filtered_df.iterrows():
                if row[col] == "Todo":
                    posibles = filtered_rvn
                    for val_col in validadores[:i]:
                        posibles = posibles[posibles[val_col] == row[val_col]]
                    posibles = posibles[col].unique()

                    if len(posibles) > 0:
                        for item in posibles:
                            new_row = row.copy()
                            new_row[col] = item
                            expanded.append(new_row)
                else:
                    expanded.append(row)

            filtered_df = pd.DataFrame(expanded)

        if selected_tipo == "Rebate":
            print("Liquidación Rebate no mapeada para SO.")

        elif selected_tipo == "Logístico CR":
            print("Liquidación Logístico CR no mapeada para SO.")

        elif selected_tipo == "Logístico Fluvial":
            print("Liquidación Logístico Fluvial no mapeada para SO.")

        elif selected_tipo == "Reconocimiento Comercial":
            merge_df = filtered_df.pivot_table(
                index=["COD_ZDES", "ETAPA", "FAMILIA", "COD_PRODUCTO"],
                # Las columnas que quieres mantener como índices
                columns="APLICACION",  # La columna que quieres pivotar
                values="VALOR",  # La columna cuyos valores serán agregados
                aggfunc="sum",  # Función de agregación (en este caso, suma)
                fill_value=0,  # Opcional: llenar con 0 los valores faltantes
            ).reset_index()
            merge_df.rename(
                columns={
                    "Precio Base": "Bonif. P.Base",
                    "Precio Neto": "Bonif. P.Neto",
                },
                inplace=True,
            )

            filtered_rvn = filtered_rvn.merge(
                mix, on=["COD_ZNJE", "COD_PRODUCTO"], how="left"
            )
            filtered_rvn = filtered_rvn.merge(
                merge_df,
                on=["COD_ZDES", "ETAPA", "FAMILIA", "COD_PRODUCTO"],
                how="inner",
            )

            for aplic in list(merge_df.columns)[4:]:
                filtered_rvn[f"APORTE {aplic}"] = (
                    filtered_rvn["PVP"]
                    * filtered_rvn["CTD_SACOS"]
                    * filtered_rvn[aplic]
                    * (
                        1
                        if aplic == "Bonif. P.Base"
                        else filtered_rvn["Dto. Factura"]
                    )
                )

            # Verificar si hay registros para la liquidación
            if filtered_rvn.shape[0] == 0:
                print("No se encontraron registros para aplicar la liquidación")
            else:
                for zdes in filtered_rvn["COD_ZDES"].unique():
                    sheet_name = "Base {}".format(
                        filtered_rvn[filtered_rvn["COD_ZDES"] == zdes][
                            "DES_ZDES"
                        ].unique()[0]
                    )
                    df_export = filtered_rvn.loc[
                        filtered_rvn["COD_ZDES"] == zdes
                    ].copy()
                    df_export.drop(["YEAR", "MONTH"], axis=1, inplace=True)
                    df_export["FECHA"] = pd.to_datetime(
                        df_export["FECHA"]
                    ).dt.strftime("%d/%m/%Y")

                    if aplication != "TMS":
                        # Determinar las posiciones de las columnas en Excel basadas en el DataFrame
                        letter_ctd = col_index_to_letter(
                            df_export.columns.get_loc("CTD_SACOS") + 1
                        )
                        letter_p_base = col_index_to_letter(
                            df_export.columns.get_loc("PVP") + 1
                        )
                        if "Bonif. P.Base" in list(merge_df.columns):
                            letter_vpb = col_index_to_letter(
                                df_export.columns.get_loc("Bonif. P.Base") + 1
                            )
                            col_aporte_vpb = (
                                df_export.columns.get_loc(
                                    "APORTE Bonif. P.Base"
                                )
                                + 1
                            )
                        if "Bonif. P.Neto" in list(merge_df.columns):
                            letter_vpn = col_index_to_letter(
                                df_export.columns.get_loc("Bonif. P.Neto") + 1
                            )
                            col_aporte_vpn = (
                                df_export.columns.get_loc(
                                    "APORTE Bonif. P.Neto"
                                )
                                + 1
                            )

                    # col_aporte = df_export.shape[1]  # La nueva columna 'APORTE' estará después de la última columna

                    df_export.rename(columns=dict_names, inplace=True)
                    df_export.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        startrow=2,
                        index=False,
                        header=False,
                    )
                    worksheet = writer.sheets[sheet_name]

                    # Escribir la fórmula en Excel para la columna APORTE
                    if "Bonif. P.Base" in list(merge_df.columns):
                        for row in range(
                            3, len(df_export) + 2
                        ):  # Suponiendo que los datos comienzan en la fila 2
                            formula = f"={letter_ctd}{row}*{letter_p_base}{row}*{letter_vpb}{row}"
                            worksheet.write_formula(
                                f"{col_index_to_letter(col_aporte_vpb)}{row}",
                                formula,
                            )
                    if "Bonif. P.Neto" in list(merge_df.columns):
                        for row in range(
                            3, len(df_export) + 2
                        ):  # Suponiendo que los datos comienzan en la fila 2
                            formula = f"={letter_ctd}{row}*{letter_p_base}{row}*{letter_vpn}{row}*(1+{letter_d_vol}{row}+{letter_d_adic}{row})"
                            worksheet.write_formula(
                                f"{col_index_to_letter(col_aporte_vpn)}{row}",
                                formula,
                            )

                    # Añadir subtotales a las columnas pertinentes
                    for col_num, col_name in enumerate(df_export.columns):
                        col_letter = col_index_to_letter(col_num + 1)
                        if col_name in [
                            "TM",
                            "Valor neto",
                            "Cantidad facturada",
                        ] + [
                            f"APORTE {aplic}"
                            for aplic in list(merge_df.columns)[4:]
                        ]:
                            formula = f"=SUBTOTAL(9, {col_letter}3:{col_letter}{len(df_export) + 2})"
                            worksheet.write(
                                0, col_num, formula, subtotal_format
                            )
                        else:
                            worksheet.write(0, col_num, "", none_format)

                    # Aplicar formato de encabezados y ajustar anchos de columnas
                    for col_num, (value, width) in enumerate(
                        zip(df_export.columns.values, get_col_widths(df_export))
                    ):  # Formato de encabezados
                        worksheet.write(1, col_num, value, header_format)
                        worksheet.set_column(col_num, col_num, width)

                    if "Bonif. P.Base" in list(merge_df.columns):
                        worksheet.write(
                            1,
                            col_aporte_vpb - 1,
                            "Importe P.Base",
                            subtotal_format,
                        )
                    if "Bonif. P.Neto" in list(merge_df.columns):
                        worksheet.write(
                            1,
                            col_aporte_vpn - 1,
                            "Importe P.Neto",
                            subtotal_format,
                        )

                    # Aplicar formato de porcentaje a 'Dto. Factura'
                    col_idx = df_export.columns.get_loc("Dto. Factura")
                    worksheet.set_column(col_idx, col_idx, 18, percent_format)

                    # Aplicar formato de porcentaje a 'Bonificación'
                    if "Bonif. P.Base" in list(merge_df.columns):
                        col_idx = df_export.columns.get_loc("Bonif. P.Base")
                        worksheet.set_column(
                            col_idx, col_idx, 18, percent_format
                        )
                    if "Bonif. P.Neto" in list(merge_df.columns):
                        col_idx = df_export.columns.get_loc("Bonif. P.Neto")
                        worksheet.set_column(
                            col_idx, col_idx, 18, percent_format
                        )

                # Agregar hoja de resumen
                if filtered_df["APLICACION"].nunique() == 1:
                    sum = (
                        filtered_rvn.groupby("DES_ZDES")
                        .agg(
                            {
                                "CTD_SACOS": "sum",
                                "TMS": "sum",
                                f"APORTE {merge_df.columns[-1]}": "sum",
                            }
                        )
                        .reset_index()
                    )
                else:
                    sum = (
                        filtered_rvn.groupby("DES_ZDES")
                        .agg(
                            {
                                "CTD_SACOS": "sum",
                                "TMS": "sum",
                                f"APORTE {merge_df.columns[-2]}": "sum",
                                f"APORTE {merge_df.columns[-1]}": "sum",
                            }
                        )
                        .reset_index()
                    )

                # Agregar filas adicionales para el resumen
                sum.rename(
                    columns={
                        "CTD_SACOS": "Cantidad sacos",
                        "DES_ZDES": "CLIENTE",
                        "TMS": "Toneladas",
                    },
                    inplace=True,
                )
                sum.loc["TOTAL", "Toneladas"] = sum["Toneladas"].sum()
                sum.loc["TOTAL", "Cantidad sacos"] = sum["Cantidad sacos"].sum()
                print(["Bonif. P.Base"] in list(merge_df.columns))
                if "Bonif. P.Base" in list(merge_df.columns):
                    sum.loc["TOTAL", "APORTE Bonif. P.Base"] = sum[
                        "APORTE Bonif. P.Base"
                    ].sum()
                if "Bonif. P.Neto" in list(merge_df.columns):
                    sum.loc["TOTAL", "APORTE Bonif. P.Neto"] = sum[
                        "APORTE Bonif. P.Neto"
                    ].sum()
                sum.loc["TOTAL", "CLIENTE"] = "Total"

                # Añadir hoja de resumen al archivo Excel
                sum.to_excel(writer, sheet_name="Resumen", index=False)
                worksheet = writer.sheets["Resumen"]

                for col_num, value in enumerate(
                    sum.columns.values
                ):  # Formato de encabezados
                    worksheet.write(0, col_num, value, header_format)

                for col_num, value in enumerate(
                    sum.iloc[-1]
                ):  # Formato de subtotales
                    worksheet.write(len(sum), col_num, value, subtotal_format)

                for col_num, width in enumerate(
                    get_col_widths(sum)
                ):  # Ajustar ancho de columnas
                    worksheet.set_column(col_num, col_num, width)

        else:
            print("Tipo de descuento no reconocido")
            df_export = filtered_rvn.copy()
            df_export.to_excel(
                writer,
                sheet_name="Reporte",
                startrow=1,
                index=False,
                header=False,
            )
            worksheet = writer.sheets["Reporte"]
            for col_num, col_name in enumerate(df_export.columns):
                # Añadir subtotales
                col_letter = col_index_to_letter(col_num + 1)
                if col_name in ["TMS", "VALOR_NETO", "CTD_SACOS"]:
                    formula = f"=SUBTOTAL(9, {col_letter}3:{col_letter}{len(df_export) + 2})"
                    worksheet.write(0, col_num, formula, subtotal_format)
                else:
                    worksheet.write(0, col_num, "", none_format)

            for col_num, (value, width) in enumerate(
                zip(df_export.columns.values, get_col_widths(df_export))
            ):
                # Formato de encabezados
                worksheet.write(1, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, width)
    writer.close()
    output.seek(0)
    excel_data: bytes = output.getvalue()
    b64: str = base64.b64encode(excel_data).decode("utf-8")
    file_name: str = f"Liq_{selected_nodo}_{selected_tipo}_{selected_month
    }{selected_year}.xlsx"
    file_path: str = f"../Export/{file_name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(output.getvalue())
    # Crear un enlace para descargar el archivo
    href: str = (
        f"data:application/vnd.openxmlformats-officedocument"
        f".spreadsheetml.sheet;base64,{b64}"
    )
    return href, file_name


if __name__ == "__main__":
    app.run_server(debug=True)

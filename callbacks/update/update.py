import pandas as pd

from pydantic import NonPositiveInt
from dash import callback, Input, Output

from engineering.transformation.preprocessing.cleaning.cleaning import clean
from engineering.extraction.extraction import extract
from config.settings import settings
from callbacks.update.options import (
    get_selected_liquidation,
    filter_binnacle,
    filter_sales,
    generate_options,
)

@callback(
    [
        Output("nodo-dropdown", "options"),
        Output("discount-type-dropdown", "options"),
        Output("year-dropdown", "options"),
        Output("month-dropdown", "options"),
        Output("sell-in-button", "className"),
        Output("sell-out-button", "className"),
    ],
    [
        Input("sell-in-button", "n_clicks"),
        Input("sell-out-button", "n_clicks"),
        Input("nodo-dropdown", "value"),
        Input("year-dropdown", "value"),
    ],
)
def update_dropdowns(
    sell_in_clicks: NonPositiveInt,
    sell_out_clicks: NonPositiveInt,
    selected_nodo: str,
    selected_year: str
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], str, str]:
    """
    Update the dropdowns according to the selected liquidation, node, year and month

    :param sell_in_clicks: The number of clicks on the 'Sell In' button
    :type sell_in_clicks: int
    :param sell_out_clicks: The number of clicks on the 'Sell Out' button
    :type sell_out_clicks: int
    :param selected_nodo: The selected node
    :type selected_nodo: str
    :param selected_year: The selected year
    :type selected_year: str
    :return: The updated options for the dropdowns
    :rtype: tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], str, str]
    """
    # Load the cleaned data
    raw_data: dict[str, pd.DataFrame] = extract(settings)
    cleaned_data: dict[str, pd.DataFrame] = clean(raw_data, settings)

    # Get the bitácora, maestro de ventas and sellout
    binnacle_df = cleaned_data['binnacle']
    sales_df = cleaned_data['sales']
    sellout_df = cleaned_data['sellout']

    # Determine which liquidation is selected
    selected_liquidation, sell_in_class, sell_out_class = get_selected_liquidation(sell_in_clicks, sell_out_clicks)

    # Filter the binnacle dataframe based on the selected liquidation and nodes that exist in the sales
    filtered_binnacle = filter_binnacle(binnacle_df, sales_df, selected_liquidation)

    # Filter the sales master with nodes that exist in the binnacle
    filtered_sales = filter_sales(sales_df, sellout_df, filtered_binnacle, selected_liquidation)

    # If a node is selected, filter the binnacle and sales master
    if selected_nodo:
        filtered_binnacle = filtered_binnacle[filtered_binnacle['DES_ZNJE'] == selected_nodo]
        filtered_sales = sales_df[sales_df['COD_ZNJE'] == filtered_binnacle[filtered_binnacle['DES_ZNJE'] == selected_nodo]['COD_ZNJE'].unique()[0]] \
            if selected_liquidation == 'Sell In' else \
            sellout_df[sellout_df['COD_ZNJE'] == filtered_binnacle[filtered_binnacle['DES_ZNJE'] == selected_nodo]['COD_ZNJE'].unique()[0]]

    # If a year is selected, filter the sales master
    if selected_year:
        filtered_sales = filtered_sales[filtered_sales['YEAR'] == selected_year]

    # Generate updated options for the dropdowns
    nodo_options, discount_type_options, year_options, month_options = generate_options(filtered_binnacle, filtered_sales)

    # Return the updated options
    return nodo_options, discount_type_options, year_options, month_options, sell_in_class, sell_out_class

    # Filtrar la bitácora según la liquidación seleccionada y nodos que existan en el maestro de ventas
    # filtered_df = bit[(bit['SI/SO'] == selected_liquidacion) & (bit['COD_ZNJE'].isin(rvn['COD_ZNJE'].unique()))]

    # Filtrar el maestro de ventas con nodos que existan en la bitácora
    # rvn_filtered = rvn[rvn['COD_ZNJE'].isin(filtered_df['COD_ZNJE'].unique())] if selected_liquidacion == 'Sell In' else \
    # rvn_so[rvn_so['COD_ZNJE'].isin(filtered_df['COD_ZNJE'].unique())]

    # Generar opciones actualizadas para el dropdown de 'Nodo'
    # nodo_options = [{'label': nodo, 'value': nodo} for nodo in filtered_df['DES_ZNJE'].unique()]

    # Filtrar bitácora y maestro de ventas según el nodo seleccionado
    # if selected_nodo:
    #     filtered_df = filtered_df[filtered_df['DES_ZNJE'] == selected_nodo]
    #     rvn_filtered = rvn[rvn['COD_ZNJE'] == filtered_df[filtered_df['DES_ZNJE'] == selected_nodo]['COD_ZNJE'].unique()[0]]\
    #         if selected_liquidacion == 'Sell In' else rvn_so[rvn_so['COD_ZNJE'] == filtered_df[filtered_df['DES_ZNJE'] == selected_nodo]['COD_ZNJE'].unique()[0]]

    # Generar opciones actualizadas para el dropdown de 'Tipo de Descuento'
    # tipo_descuento_options = [{'label': tipo, 'value': tipo} for tipo in filtered_df['TIPO_DESCUENTO'].unique()]

    # Generar opciones actualizadas para el dropdown de 'Año'
    # year_options = [{'label': year, 'value': year} for year in rvn_filtered['YEAR'].unique()]

    # Filtrar maestro de ventas según el año seleccionado
    # if selected_year:
    #     rvn_filtered = rvn_filtered[rvn_filtered['YEAR'] == selected_year]

    # Generar opciones actualizadas para el dropdown de 'Mes'
    # month_options = [{'label': month, 'value': month} for month in rvn_filtered['MONTH'].unique()]

    # Retornar las opciones actualizadas
    # return nodo_options, tipo_descuento_options, year_options, month_options, sell_in_class, sell_out_class
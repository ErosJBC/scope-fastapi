import pandas as pd

from pydantic import NonPositiveInt
from dash import callback, Input, Output

from callbacks.update.options.filter import (
    filter_binnacle,
    filter_sales,
)
from callbacks.update.options.options import (
    get_selected_liquidation,
    generate_options,
)
from config.settings import settings
from constants.constants import constants
from engineering.extraction.extraction import extract
from engineering.transformation.preprocessing.preprocessing import preprocess


@callback(
    [
        Output(item["component_id"], item["component_property"]) for item in constants.OUTPUT_UDPATE
    ],
    [
        Input(item["component_id"], item["component_property"]) for item in constants.INPUT_UPDATE
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
    raw_data: dict[str, pd.DataFrame] = extract(settings)
    preprocessed_data: dict[str, pd.DataFrame] = preprocess(raw_data, settings)

    selected_liquidation, sell_in_class, sell_out_class = get_selected_liquidation(sell_in_clicks, sell_out_clicks)
    filtered_binnacle = filter_binnacle(preprocessed_data['binnacle'], preprocessed_data['sales'], selected_liquidation)
    filtered_sales = filter_sales(preprocessed_data['sales'], preprocessed_data['sellout'], filtered_binnacle, selected_liquidation)

    if selected_nodo:
        filtered_binnacle = filtered_binnacle[filtered_binnacle['DES_ZNJE'] == selected_nodo]
        filtered_sales = preprocessed_data['sales'][
            preprocessed_data['sales']['COD_ZNJE'] == filtered_binnacle[filtered_binnacle['DES_ZNJE'] == selected_nodo]['COD_ZNJE'].unique()[0]
        ]\
            if selected_liquidation == 'Sell In' else \
            preprocessed_data['sellout'][
                preprocessed_data['sellout']['COD_ZNJE'] == filtered_binnacle[filtered_binnacle['DES_ZNJE'] == selected_nodo]['COD_ZNJE'].unique()[0]
            ]

    if selected_year:
        filtered_sales = filtered_sales[filtered_sales['YEAR'] == selected_year]

    nodo_options, discount_type_options, year_options, month_options = generate_options(filtered_binnacle, filtered_sales)

    return nodo_options, discount_type_options, year_options, month_options, sell_in_class, sell_out_class

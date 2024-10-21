import pandas as pd

def get_selected_liquidation(sell_in_clicks: int, sell_out_clicks: int) -> tuple[str, str, str]:
    """
    Determine which liquidation is selected

    :param sell_in_clicks: The number of clicks on the 'Sell In' button
    :type sell_in_clicks: int
    :param sell_out_clicks: The number of clicks on the 'Sell Out' button
    :type sell_out_clicks: int
    :return: The selected liquidation, the class for the 'Sell In' button and the class for the 'Sell Out' button
    :rtype: tuple[str, str, str]
    """
    selected_liquidation: str
    sell_in_class: str
    sell_out_class: str
    if sell_in_clicks < sell_out_clicks:
        selected_liquidation = "Sell Out"
        sell_in_class = "btn btn-secondary"
        sell_out_class = "btn btn-primary"
    else:
        selected_liquidation = "Sell In"
        sell_in_class = "btn btn-primary"
        sell_out_class = "btn btn-secondary"
    return selected_liquidation, sell_in_class, sell_out_class

def generate_options(
    filtered_binnacle: pd.DataFrame,
    filtered_sales: pd.DataFrame
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """
    Generate updated options for the dropdowns

    :param filtered_binnacle: The filtered dataframe
    :type filtered_binnacle: pd.DataFrame
    :param filtered_sales: The filtered dataframe
    :type filtered_sales: pd.DataFrame
    :return: The updated options for the dropdowns
    :rtype: tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]
    """
    nodo_options: list[dict[str, str]] = [
        {"label": nodo, "value": nodo} for nodo in filtered_binnacle["DES_ZNJE"].unique()
    ]
    discount_type_options: list[dict[str, str]] = [
        {"label": discount_type, "value": discount_type}
        for discount_type in filtered_binnacle["TIPO_DESCUENTO"].unique()
    ]
    year_options: list[dict[str, str]] = [
        {"label": year, "value": year} for year in filtered_sales["YEAR"].unique()
    ]
    month_options: list[dict[str, str]] = [
        {"label": month, "value": month} for month in filtered_sales["MONTH"].unique()
    ]
    return nodo_options, discount_type_options, year_options, month_options
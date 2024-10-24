"""
A module for integration in the engineering.transformation.integration package.
"""

import pandas as pd
from typing import Any

from engineering.transformation.integration.binnacle import BinnacleIntegrator
from engineering.transformation.integration.discount_type.sellout import generate_sellout_sheets
from engineering.transformation.integration.sellin import SellinIntegrator
from engineering.transformation.integration.discount_type.rebate.rebate_type import generate_rebate_sheets
from engineering.transformation.integration.discount_type.other_type import generate_other_discount_type_sheets
from engineering.transformation.integration.sellout import SellOutIntegrator
from schemas.request.options import Options


def integrate_sellin(
    data: dict[str, pd.DataFrame],
    options: Options
) -> dict[str, pd.DataFrame]:
    """
    Integrate sellin with another dataframes

    :param data: The dataframes to integrate
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: Options
    :return: The integrated dataframe with sellin info
    :rtype: dict[str, pd.DataFrame]
    """
    sellin_data = data["sales"].copy()
    list_month: list[str] = BinnacleIntegrator.get_list_month_by_period(data["binnacle"], options.month)  # type: ignore
    filtered_sellin = SellinIntegrator.filter_options(sellin_data, options, list_month)
    data.update({"sales": filtered_sellin})

    sheets: dict[str, pd.DataFrame]
    if options.discount_type == "Rebate":
        sheets = generate_rebate_sheets(data, options, list_month)
    else:
        sheets = generate_other_discount_type_sheets(data, options, list_month)
    return sheets

def integrate_sellout(
    data: dict[str, pd.DataFrame],
    options: Options
) -> dict[str, pd.DataFrame]:
    """
    Integrate sellout with another dataframes

    :param data: The required data to integrate
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: Options
    :return: The integrated dataframe with sellout info
    :rtype: tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]
    """
    sellout_data = data["sellout"].copy()
    binnacle_data = data["binnacle"].copy()
    sellout_integrator: SellOutIntegrator = SellOutIntegrator(sellout_data)
    list_month: list[str] = BinnacleIntegrator.get_list_month_by_period(binnacle_data, options.month)  # type: ignore
    format_binnacle = BinnacleIntegrator.overwrite_family(binnacle_data)
    filtered_sellout = sellout_integrator.filter_options(format_binnacle, options, list_month)
    filtered_sellout["COD_ZDES"] = filtered_sellout["COD_ZDES"].astype(int)
    data.update({"sellout": filtered_sellout})

    sheets = generate_sellout_sheets(data, options)
    return sheets

def integrate(
    data: dict[str, pd.DataFrame],
    options: Options
) -> dict[str, pd.DataFrame]:
    """
    Integrate process for transformation step

    :param data: The data to use for integration process
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: dict[str, Any]
    :return: The integrated data to load
    :rtype: dict[str, pd.DataFrame]
    """
    binnacle_data: pd.DataFrame = data["binnacle"].copy()
    filtered_binnacle: pd.DataFrame = BinnacleIntegrator.filter_options(binnacle_data, options)
    data.update({"binnacle": filtered_binnacle})

    integrated_data: dict[str, pd.DataFrame]
    if options.liquidation == "Sell In":
        integrated_data = integrate_sellin(data, options)
    else:
        integrated_data = integrate_sellout(data, options)
    return integrated_data

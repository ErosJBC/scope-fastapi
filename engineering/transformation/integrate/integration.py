"""
A module for integration in the engineering.transformation.integration package.
"""

import logging

import pandas as pd
from typing import Any

from core.decorators import with_logging
from engineering.transformation.integrate.binnacle import BinnacleIntegrator
from engineering.transformation.integrate.discount_type.sellout import generate_sellout_sheets
from engineering.transformation.integrate.sellin import SellinIntegrator
from engineering.transformation.integrate.discount_type.rebate.rebate_type import generate_rebate_sheets
from engineering.transformation.integrate.discount_type.other_type import generate_other_discount_type_sheets
from engineering.transformation.integrate.sellout import SellOutIntegrator

logger: logging.Logger = logging.getLogger(__name__)


def integrate_sellin(
    data: dict[str, pd.DataFrame],
    options: dict[str, Any]
) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
    """
    Integrate sellin with another dataframes

    :param data: The dataframes to integrate
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: dict[str, Any]
    :return: The integrated dataframe with sellin info
    :rtype: tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]
    """
    sellin_data = data["sales"].copy()
    filtered_sellin = SellinIntegrator.filter_options(sellin_data, options)
    data.update({"sales": filtered_sellin})

    sheets: dict[str, pd.DataFrame]
    data: dict[str, pd.DataFrame]
    if options["discount_type"] == "Rebate":
        sheets = generate_rebate_sheets(data, options)
    else:
        sheets = generate_other_discount_type_sheets(data, options)
    return sheets, data

def integrate_sellout(
    data: dict[str, pd.DataFrame],
    options: dict[str, Any]
) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
    """
    Integrate sellout with another dataframes

    :param data: The required data to integrate
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: dict[str, Any]
    :return: The integrated dataframe with sellout info
    :rtype: tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]
    """
    sellout_data = data["sellout"].copy()
    format_sellout = BinnacleIntegrator.overwrite_family(sellout_data)
    filtered_sellout = SellOutIntegrator.filter_options(format_sellout, options)
    filtered_sellout["COD_ZDES"] = filtered_sellout["COD_ZDES"].astype(int)
    data.update({"sellout": filtered_sellout})

    sheets, data = generate_sellout_sheets(data, options)
    return sheets, data

@with_logging
def integrate(
    data: dict[str, pd.DataFrame],
    options: dict[str, Any]
) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
    """
    Integrate process for transformation step

    :param data: The data to use for integration process
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: dict[str, Any]
    :return: The integrated data to load
    :rtype: dict[str, pd.DataFrame]
    """
    options["selected_liquidation"] = "Sell Out" if options["sell_in_clicks"] < options["sell_out_clicks"] else 'Sell In'
    binnacle_data: pd.DataFrame = data["binnacle"].copy()
    filtered_binnacle: pd.DataFrame = BinnacleIntegrator.filter_options(binnacle_data, options)
    if options["nodo"] != "D. COPACIGULF":
        filtered_binnacle = BinnacleIntegrator.create_validators_column(filtered_binnacle, data["sales"])
    data.update({"binnacle": filtered_binnacle})

    options["list_months"] = BinnacleIntegrator.get_list_month_by_period(filtered_binnacle, options["month"])

    integrated_data: dict[str, pd.DataFrame]
    data_additional: dict[str, pd.DataFrame]
    if options["selected_liquidation"] == "Sell In":
        integrated_data, data_additional = integrate_sellin(data, options)
    else:
        integrated_data, data_additional = integrate_sellout(data, options)
    logger.info("Integration finished")
    return integrated_data, data_additional

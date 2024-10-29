"""
This module contains the functions to generate the sheets for the fluvial logistic discount type
"""

import pandas as pd

from engineering.transformation.integration.discount_type.fluvial_logistic.fluvial import FluvialLogisticSellinIntegrator
from engineering.transformation.integration.discount_type.summary import generate_summary_cr_fluvial_logistic_sheet
from engineering.transformation.integration.utils.utils import generate_base_months_sheets
from schemas.request.options import Options


def generate_fluvial_logistic_sheets(
    data: dict[str, pd.DataFrame],
    options: Options,
    list_month: list[int]
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the fluvial logistic discount type

    :param data: The dataframes to integrate
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: Options
    :param list_month: The list of months
    :type list_month: list[int]
    :return: The sheets for the fluvial logistic discount type
    :rtype: dict[str, pd.DataFrame]
    """
    sellin = data["sales"].copy()
    fluvial_logistic: FluvialLogisticSellinIntegrator = FluvialLogisticSellinIntegrator()
    sellin = fluvial_logistic.add_contribution_column(sellin)
    base_sheets: dict[str, pd.DataFrame] = generate_base_months_sheets(sellin, options, list_month)
    summary_sheet: dict[str, pd.DataFrame] = generate_summary_cr_fluvial_logistic_sheet(sellin)
    dict_sheets = {**base_sheets, **summary_sheet}
    return dict_sheets

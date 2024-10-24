"""
This module is responsible for generating the sheets for the cr logistic discount type
"""

import pandas as pd

from engineering.transformation.integration.discount_type.cr_logistic.cr import CrLogisticSellinIntegrator
from engineering.transformation.integration.discount_type.summary import generate_summary_cr_fluvial_logistic_sheet
from engineering.transformation.integration.utils.utils import generate_base_months_sheets
from schemas.request.options import Options


def generate_cr_logistic_sheets(
    data: dict[str, pd.DataFrame],
    options: Options,
    list_month: list[str]
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the cr logistic discount type

    :param data: The dataframes to integrate
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: Options
    :param list_month: The list of months
    :type list_month: list[str]
    :return: The sheets for the cr logistic discount type
    :rtype: dict[str, pd.DataFrame]
    """
    sellin = data["sales"].copy()
    sellin['Bonificación'] = pd.to_numeric(sellin['Bonificación'].apply(
        lambda x: str(x).replace("$", "").replace(",", ".")
    ))
    cr_logistic: CrLogisticSellinIntegrator = CrLogisticSellinIntegrator()
    sellin = cr_logistic.add_contribution_column(sellin)
    sellin = cr_logistic.filter_ref_order(sellin)
    base_sheets: dict[str, pd.DataFrame] = generate_base_months_sheets(sellin, options, list_month)
    summary_sheet: dict[str, pd.DataFrame] = generate_summary_cr_fluvial_logistic_sheet(sellin)
    dict_sheets = {**base_sheets, **summary_sheet}
    return dict_sheets

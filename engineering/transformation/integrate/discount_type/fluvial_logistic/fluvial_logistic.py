import pandas as pd

from typing import Any

from engineering.transformation.integrate.discount_type.fluvial_logistic.fluvial import FluvialLogisticSellinIntegrator
from engineering.transformation.integrate.discount_type.summary import generate_summary_cr_fluvial_logistic_sheet
from engineering.transformation.integrate.utils.utils import generate_base_months_sheets


def generate_fluvial_logistic_sheets(
    data: dict[str, pd.DataFrame],
    options: dict[str, Any]
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the fluvial logistic discount type

    :param data: The dataframes to integrate
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: dict[str, Any]
    :return: The sheets for the fluvial logistic discount type
    :rtype: dict[str, pd.DataFrame]
    """
    sellin_df = data["sales"].copy()
    fluvial_logistic: FluvialLogisticSellinIntegrator = FluvialLogisticSellinIntegrator()
    sellin_df = fluvial_logistic.add_contribution_column(sellin_df)
    base_sheets: dict[str, pd.DataFrame] = generate_base_months_sheets(sellin_df, options)
    summary_sheet: dict[str, pd.DataFrame] = generate_summary_cr_fluvial_logistic_sheet(sellin_df)
    dict_sheets = {**base_sheets, **summary_sheet}
    return dict_sheets
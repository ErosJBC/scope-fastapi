import pandas as pd

from typing import Any

from engineering.transformation.integrate.discount_type.cr_logistic.cr import CrLogisticSellinIntegrator
from engineering.transformation.integrate.discount_type.summary import generate_summary_cr_fluvial_logistic_sheet
from engineering.transformation.integrate.utils.utils import generate_base_months_sheets


def generate_cr_logistic_sheets(
    data: dict[str, pd.DataFrame],
    options: dict[str, Any]
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the cr logistic discount type

    :param data: The dataframes to integrate
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: dict[str, Any]
    :return: The sheets for the cr logistic discount type
    :rtype: dict[str, pd.DataFrame]
    """
    sellin_df = data["sales"].copy()
    cr_logistic: CrLogisticSellinIntegrator = CrLogisticSellinIntegrator()
    sellin_df = cr_logistic.add_contribution_column(sellin_df)
    sellin_df = cr_logistic.filter_ref_order(sellin_df)
    base_sheets: dict[str, pd.DataFrame] = generate_base_months_sheets(sellin_df, options)
    summary_sheet: dict[str, pd.DataFrame] = generate_summary_cr_fluvial_logistic_sheet(sellin_df)
    dict_sheets = {**base_sheets, **summary_sheet}
    return dict_sheets
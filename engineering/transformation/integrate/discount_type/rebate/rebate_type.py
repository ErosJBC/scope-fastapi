import pandas as pd

from typing import Any

from engineering.transformation.integrate.binnacle import BinnacleIntegrator
from engineering.transformation.integrate.discount_type.rebate.rebate import RebateSellinIntegrator
from engineering.transformation.integrate.discount_type.summary import generate_summary_rebate_sheet
from engineering.transformation.integrate.utils.utils import generate_base_months_sheets


def generate_rebate_sheets(
    data: dict[str, pd.DataFrame],
    options: dict[str, Any]
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the rebate report

    :param data: The data to generate the sheets
    :type data: dict[str, pd.DataFrame]
    :param options: The options selected by the user
    :type options: dict[str, Any]
    :return: The sheets for the rebate report
    :rtype: dict[str, pd.DataFrame]
    """
    binnacle_df: pd.DataFrame = data["binnacle"].copy()
    sellin_df: pd.DataFrame = data["sales"].copy()
    if options["nodo"] == "D. COPACIGULF":
        binnacle_df = BinnacleIntegrator.create_lower_tm_column(binnacle_df)
        binnacle_df = BinnacleIntegrator.create_upper_tm_column(binnacle_df)
        binnacle_df = BinnacleIntegrator.create_mean_tm_column(binnacle_df, sellin_df)
    else:
        rebate: RebateSellinIntegrator = RebateSellinIntegrator()
        sellin_df = rebate.merge_dataframes(sellin_df, binnacle_df)
        application = BinnacleIntegrator.get_type_application(binnacle_df)
        if application != "TMS":
            sellin_df = rebate.add_pvp_column(sellin_df)
            sellin_df = rebate.add_discount_column(sellin_df)
            sellin_df = rebate.add_credit_column(sellin_df)
            sellin_df = rebate.add_additional_discount_column(sellin_df)

        sellin_df = rebate.add_contribution_column(sellin_df, application)

    base_sheets: dict[str, pd.DataFrame] = generate_base_months_sheets(sellin_df, options)
    summary_sheet: dict[str, pd.DataFrame] = generate_summary_rebate_sheet(sellin_df, binnacle_df, options)
    dict_sheets: dict[str, pd.DataFrame] = {**base_sheets, **summary_sheet}
    return dict_sheets


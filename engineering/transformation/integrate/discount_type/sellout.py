import pandas as pd

from typing import Any

from engineering.transformation.integrate.discount_type.summary import generate_summary_sellout_sheet
from engineering.transformation.integrate.sellout import SellOutIntegrator
from engineering.transformation.integrate.utils.utils import generate_base_months_sheets


def generate_sellout_sheets(
    data: dict[str, pd.DataFrame], options: dict[str, Any]
) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
    """
    Generate the sellout sheets for the transformation

    :param data: The data to use for the transformation
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: dict[str, Any]
    :return: The transformed data
    :rtype: tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]
    """
    sellout_df: pd.DataFrame = data["sellout"].copy()
    prices_df: pd.DataFrame = data["prices"].copy()

    pivot_df: pd.DataFrame = SellOutIntegrator.pivot_dataframe(sellout_df)
    merged_df: pd.DataFrame = SellOutIntegrator.merge_with_prices_dataframe(sellout_df, prices_df)
    merged_df = SellOutIntegrator.merge_with_pivot_dataframe(merged_df, pivot_df)
    final_df = SellOutIntegrator.add_contribution_column(merged_df)

    base_sheets: dict[str, pd.DataFrame] = generate_base_months_sheets(final_df, options)
    summary_sheet: dict[str, pd.DataFrame] = generate_summary_sellout_sheet(final_df, pivot_df)
    dict_sheets: dict[str, pd.DataFrame] = {**base_sheets, **summary_sheet}
    data_additional: dict[str, pd.DataFrame] = {"pivot": pivot_df, "binnacle": data["binnacle"]}
    return dict_sheets, data_additional

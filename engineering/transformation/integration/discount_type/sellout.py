"""
This module is responsible for generating the sellout sheets for the transformation
"""

import pandas as pd

from engineering.transformation.integration.binnacle import BinnacleIntegrator
from engineering.transformation.integration.discount_type.summary import generate_summary_sellout_sheet
from engineering.transformation.integration.sellout import SellOutIntegrator
from engineering.transformation.integration.utils.utils import generate_base_zdes_sheets
from schemas.request.options import Options


def generate_sellout_sheets(
    data: dict[str, pd.DataFrame],
    options: Options
) -> dict[str, pd.DataFrame]:
    """
    Generate the sellout sheets for the transformation

    :param data: The data to use for the transformation
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: dict[str, Any]
    :return: The transformed data
    :rtype: dict[str, pd.DataFrame]
    """
    binnacle: pd.DataFrame = data["binnacle"].copy()
    sellout: pd.DataFrame = data["sellout"].copy()
    prices: pd.DataFrame = data["prices"].copy()
    binnacle = BinnacleIntegrator.create_validators_column(binnacle, sellout, True)
    sellout_integrator: SellOutIntegrator = SellOutIntegrator(sellout)

    pivot_df: pd.DataFrame = BinnacleIntegrator.pivot_dataframe(binnacle)
    merged_df: pd.DataFrame = sellout_integrator.merge_with_prices_dataframe(prices)
    merged_df = sellout_integrator.merge_with_pivot_dataframe(merged_df, pivot_df)
    final_df = sellout_integrator.add_contribution_column(pivot_df.columns, merged_df)

    base_sheets: dict[str, pd.DataFrame] = generate_base_zdes_sheets(final_df)
    summary_sheet: dict[str, pd.DataFrame] = generate_summary_sellout_sheet(binnacle, final_df, pivot_df)
    dict_sheets: dict[str, pd.DataFrame] = {**base_sheets, **summary_sheet, "pivot": pivot_df}
    return dict_sheets

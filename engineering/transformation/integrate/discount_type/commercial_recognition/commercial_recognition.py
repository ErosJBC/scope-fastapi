import pandas as pd

from typing import Any

from engineering.transformation.integrate.binnacle import BinnacleIntegrator
from engineering.transformation.integrate.discount_type.commercial_recognition.commercial import \
    CommercialRecognitionSellinIntegrator
from engineering.transformation.integrate.discount_type.summary import generate_summary_commercial_recognition_sheet
from engineering.transformation.integrate.utils.utils import generate_base_months_sheets


def generate_commercial_recognition_sheets(
    data: dict[str, pd.DataFrame],
    options: dict[str, Any]
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the commercial recognition discount type

    :param data: The dataframes to integrate
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: dict[str, Any]
    :return: The sheets for the commercial recognition discount type
    :rtype: dict[str, pd.DataFrame]
    """
    binnacle_df = data["binnacle"].copy()
    sellin_df = data["sales"].copy()
    application = BinnacleIntegrator.get_type_application(binnacle_df)
    commercial_recognition: CommercialRecognitionSellinIntegrator = CommercialRecognitionSellinIntegrator()
    if application != "TMS":
        sellin_df = commercial_recognition.add_pvp_column(sellin_df)
        sellin_df = commercial_recognition.add_discount_column(sellin_df)

    sellin_df = commercial_recognition.add_credit_column(sellin_df, application)
    sellin_df = commercial_recognition.add_additional_discount_column(sellin_df)
    sellin_df = commercial_recognition.add_contribution_column(sellin_df, application)
    base_sheets: dict[str, pd.DataFrame] = generate_base_months_sheets(sellin_df, options)
    summary_sheet: dict[str, pd.DataFrame] = generate_summary_commercial_recognition_sheet(sellin_df)
    dict_sheets = {**base_sheets, **summary_sheet}
    return dict_sheets

"""
This module contains the class to integrate the Commercial Recognition sellin data.
"""

import pandas as pd

from engineering.transformation.integration.binnacle import BinnacleIntegrator
from engineering.transformation.integration.discount_type.commercial_recognition.commercial import \
    CommercialRecognitionSellinIntegrator
from engineering.transformation.integration.discount_type.summary import generate_summary_commercial_recognition_sheet
from engineering.transformation.integration.sellin import SellinIntegrator
from engineering.transformation.integration.utils.utils import generate_base_months_sheets
from schemas.request.options import Options


def generate_commercial_recognition_sheets(
    data: dict[str, pd.DataFrame],
    options: Options,
    list_month: list[int]
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the commercial recognition discount type

    :param data: The dataframes to integrate
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: Options
    :param list_month: The list of months
    :type list_month: list[int]
    :return: The sheets for the commercial recognition discount type
    :rtype: dict[str, pd.DataFrame]
    """
    binnacle = data["binnacle"].copy()
    sellin = data["sales"].copy()
    application = BinnacleIntegrator.get_type_application(binnacle)
    commercial_recognition: CommercialRecognitionSellinIntegrator = CommercialRecognitionSellinIntegrator()
    if application == "TMS":
        sellin = SellinIntegrator.convert_bonus_column(sellin)
    else:
        sellin["Bonificación"] = pd.to_numeric(sellin["Bonificación"])
        sellin = commercial_recognition.add_pvp_column(sellin)
        sellin = commercial_recognition.add_discount_column(sellin)
        sellin = commercial_recognition.add_credit_column(sellin, application)
        sellin = commercial_recognition.add_additional_discount_column(sellin)

    sellin = commercial_recognition.add_contribution_column(sellin, application)
    base_sheets: dict[str, pd.DataFrame] = generate_base_months_sheets(sellin, options, list_month)
    summary_sheet: dict[str, pd.DataFrame] = generate_summary_commercial_recognition_sheet(sellin)
    dict_sheets = {**base_sheets, **summary_sheet}
    return dict_sheets

"""
This module is used to generate the sheets for the other discount type
"""

import pandas as pd

from engineering.transformation.integration.binnacle import BinnacleIntegrator
from engineering.transformation.integration.discount_type.commercial_recognition.commercial_recognition import \
    generate_commercial_recognition_sheets
from engineering.transformation.integration.discount_type.cr_logistic.cr_logistic import generate_cr_logistic_sheets
from engineering.transformation.integration.discount_type.fluvial_logistic.fluvial_logistic import \
    generate_fluvial_logistic_sheets
from engineering.transformation.integration.sellin import SellinIntegrator
from schemas.request.options import Options


def generate_other_discount_type_sheets(
    data: dict[str, pd.DataFrame],
    options: Options,
    list_month: list[str]
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the other discount type

    :param data: The dataframes to integrate
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: Options
    :param list_month: The list of months
    :type list_month: list[str]
    :return: The sheets for the other discount type
    :rtype: dict[str, pd.DataFrame]
    """
    binnacle: pd.DataFrame = data["binnacle"].copy()
    sellin: pd.DataFrame = data["sales"].copy()
    validators_data: pd.DataFrame = BinnacleIntegrator.create_validators_column(binnacle, sellin)
    merged_data: pd.DataFrame = SellinIntegrator.merge_dataframes(sellin, validators_data)
    data.update({"binnacle": validators_data})
    data.update({"sales": merged_data})
    dict_sheets: dict[str, pd.DataFrame] = {}
    if options.discount_type == "Logístico CR":
        dict_sheets = generate_cr_logistic_sheets(data, options, list_month)
    elif options.discount_type == "Logístico Fluvial":
        dict_sheets = generate_fluvial_logistic_sheets(data, options, list_month)
    elif options.discount_type == "Reconocimiento Comercial":
        dict_sheets = generate_commercial_recognition_sheets(data, options, list_month)
    return dict_sheets

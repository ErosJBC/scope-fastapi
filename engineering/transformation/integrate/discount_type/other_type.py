import pandas as pd

from typing import Any

from engineering.transformation.integrate.discount_type.commercial_recognition.commercial_recognition import \
    generate_commercial_recognition_sheets
from engineering.transformation.integrate.discount_type.cr_logistic.cr_logistic import generate_cr_logistic_sheets
from engineering.transformation.integrate.discount_type.fluvial_logistic.fluvial_logistic import \
    generate_fluvial_logistic_sheets
from engineering.transformation.integrate.sellin import SellinIntegrator


def generate_other_discount_type_sheets(
    data: dict[str, pd.DataFrame],
    options: dict[str, Any]
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the other discount type

    :param data: The dataframes to integrate
    :type data: dict[str, pd.DataFrame]
    :param options: The selected options for the transformation
    :type options: dict[str, Any]
    :return: The sheets for the other discount type
    :rtype: dict[str, pd.DataFrame]
    """
    binnacle_df: pd.DataFrame = data["binnacle"].copy()
    sellin_df: pd.DataFrame = data["sales"].copy()
    merged_df: pd.DataFrame = SellinIntegrator.merge_dataframes(sellin_df, binnacle_df)
    data.update({"sales": merged_df})
    dict_sheets: dict[str, pd.DataFrame] = {}
    if options["discount_type"] == "Logístico CR":
        dict_sheets = generate_cr_logistic_sheets(data, options)
    elif options["discount_type"] == "Logístico Fluvial":
        dict_sheets = generate_fluvial_logistic_sheets(data, options)
    elif options["discount_type"] == "Reconocimiento Comercial":
        dict_sheets = generate_commercial_recognition_sheets(data, options)
    return dict_sheets
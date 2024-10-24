"""
A module for transformation in the engineering-transformation package.
"""

import pandas as pd

from config.settings import Settings
from engineering.transformation.integration.integration import integrate
from engineering.transformation.preprocessing.preprocessing import preprocess
from schemas.request.options import Options


def transform(
    raw_data: dict[str, pd.DataFrame],
    settings: Settings,
    options: Options
) -> dict[str, pd.DataFrame]:
    """
    Transformation step on the ETL pipeline to get more detailed data

    :param raw_data: The raw data to be transformed
    :type raw_data: dict[str, pd.DataFrame]
    :param settings: The settings for the transformation process
    :type settings: Settings
    :param options: The selected options for the transformation
    :type options: dict[str, Any]
    :return: The transformed data
    :rtype: tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]
    """
    preprocessed_data: dict[str, pd.DataFrame] = preprocess(raw_data, settings)
    integrated_data = integrate(preprocessed_data, options)
    return integrated_data

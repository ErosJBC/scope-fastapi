"""
A module for transformation in the engineering-transformation package.
"""

import logging

import pandas as pd
from typing import Any

from config.settings import Settings
from core.decorators import with_logging
from engineering.transformation.integrate.integration import integrate
from engineering.transformation.preprocessing.preprocessing import preprocess

logger: logging.Logger = logging.getLogger(__name__)


@with_logging
def transform(
    raw_data: dict[str, pd.DataFrame],
    settings: Settings,
    options: dict[str, Any]
) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
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
    integrated_data, data_additional = integrate(preprocessed_data, options)
    logging.info("Data transformations applied")
    return integrated_data, data_additional

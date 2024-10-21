"""
A module for preprocessing in the engineering.transformation.preprocessing
 package.
"""

import logging

import pandas as pd

from config.settings import Settings
from core.decorators import with_logging
from engineering.transformation.preprocessing.cleaning.cleaning import clean
from engineering.transformation.preprocessing.integration.integration import integrate

logger: logging.Logger = logging.getLogger(__name__)


@with_logging
def preprocess(
    raw_data: dict[str, pd.DataFrame], settings: Settings
) -> dict[str, pd.DataFrame]:
    """
    Preprocess the raw data to be transformed into the detailed data
    representation

    :param raw_data: The raw data to be preprocessed
    :type raw_data: dict[str, pd.DataFrame]
    :param settings: The required settings to transform the data
    :type settings: Settings
    :return: The preprocessed data as a dictionary with the same keys from
    the raw data
    :rtype: dict[str, pd.DataFrame]
    """
    cleaned_data: dict[str, pd.DataFrame] = clean(raw_data, settings)
    updated_data: dict[str, pd.DataFrame] = cleaned_data.copy()
    reduced_data: dict[str, pd.DataFrame] = integrate(cleaned_data, settings)
    updated_data.update(reduced_data)

    logger.info("Preprocessing finished")
    return updated_data

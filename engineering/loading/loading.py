"""
A module for loading in the engineering-loading package.
"""

import logging

import pandas as pd
from pydantic import FilePath, NewPath, PositiveInt
from typing import Any

from config.settings import GeneralSettings
from utils.utils import save_dataframes_to_excel

logger: logging.Logger = logging.getLogger(__name__)


def load(
    transformed_data: dict[str, pd.DataFrame],
    data_additional: dict[str, pd.DataFrame],
    general_settings: GeneralSettings,
    options: dict[str, Any],
) -> tuple[str, str]:
    """
    Load dataframes into an Excel file and apply formatting.

    :param transformed_data: A dictionary with keys as sheet names and values as dataframes.
    :type transformed_data: dict[str, pd.DataFrame]
    :param data_additional: Additional data to be saved
    :type data_additional: dict[str, pd.DataFrame]
    :param general_settings: The general settings required to load the
    dataframes
    :type general_settings: GeneralSettings
    :param options: The selected options
    :type options: dict[str, Any]
    :return: The path where the data has been saved and the updated output filename
    :rtype: tuple[str, str]
    """

    save_dataframes_to_excel(transformed_data, data_additional, options)
    # format_workbook(data, path)
    logging.info("Data has been loaded successfully")

    return "path", "filename"

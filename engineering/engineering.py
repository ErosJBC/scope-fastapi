"""
A module for pipeline in the engineering package.
"""

import logging

import pandas as pd

from typing import Any

from config.settings import Settings
from engineering.extraction.extraction import extract
from engineering.loading.loading import load
from engineering.transformation.transformation import transform

logger: logging.Logger = logging.getLogger(__name__)


def run_generate_data(options: dict[str, Any], settings: Settings) -> tuple[str, str]:
    """
    Executes the extraction, transformation and loading steps from the pipeline

    :options: The selected options
    :type options: dict[str, Any]
    :param settings: The settings required for the pipeline execution
    :type settings: Settings
    :return: Return the file in base64 and the file name
    :rtype: tuple[str, str]
    """
    logger.info("Starting the process.")
    raw_data: dict[str, pd.DataFrame] = extract(settings)
    transformed_data, data_additional = transform(raw_data, settings, options)
    file_b64, filename = load(transformed_data, data_additional, settings.general, options)
    logging.info("Process finished")
    return file_b64, filename

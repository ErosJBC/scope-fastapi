"""
A module for pipeline in the engineering package.
"""

import pandas as pd

from config.settings import Settings
from engineering.extraction.extraction import extract
from engineering.transformation.integration.integration import integrate
from engineering.transformation.preprocessing.preprocessing import preprocess
from engineering.loading.loading import load
from schemas.request.options import Options
from engineering.loading.utils import save_dataframes_to_parquet


def run_load_data(settings: Settings) -> None:
    """
    Executes the extraction, transformation and loading steps from the pipeline

    :param settings: The settings required for the pipeline execution
    :type settings: Settings
    :return: Return the file in base64 and the file name
    :rtype: tuple[str, str]
    """
    raw_data: dict[str, pd.DataFrame] = extract(settings)
    preprocessed_data = preprocess(raw_data, settings)
    save_dataframes_to_parquet(preprocessed_data, settings.general)

def run_process_data(
    dataframes: dict[str, pd.DataFrame],
    settings: Settings,
    options: Options
) -> tuple[str, str]:
    """
    Generate the data based on the selected options.

    :param dataframes: The dataframes to generate the data
    :type dataframes: dict[str, pd.DataFrame]
    :param settings: The settings required for the pipeline execution
    :type settings: Settings
    :param options: The selected options for the transformation
    :type options: Options
    :return: Return the file in base64 and the file name
    :rtype: tuple[str, str]
    """
    integrated_data: dict[str, pd.DataFrame] = integrate(dataframes, options)
    file_name, file_base64 = load(integrated_data, settings.general, options)
    return file_name, file_base64
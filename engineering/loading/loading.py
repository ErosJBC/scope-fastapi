"""
A module for loading in the engineering-loading package.
"""
import base64
import logging

import pandas as pd
from pydantic import FilePath, NewPath

from config.settings import GeneralSettings
from engineering.loading.formatting.formatting import format_worksheet
from schemas.request.options import Options
from engineering.loading.utils import save_dataframes_to_excel, generate_output_filename

logger: logging.Logger = logging.getLogger(__name__)


def load(
    transformed_data: dict[str, pd.DataFrame],
    general_settings: GeneralSettings,
    options: Options,
) -> tuple[str, str]:
    """
    Load dataframes into an Excel file and apply formatting.

    :param transformed_data: A dictionary with keys as sheet names and values as dataframes.
    :type transformed_data: dict[str, pd.DataFrame]
    :param general_settings: The general settings required to load the
    dataframes
    :type general_settings: GeneralSettings
    :param options: The selected options
    :type options: dict[str, Any]
    :return: The path where the data has been saved and the updated output filename
    :rtype: tuple[str, str]
    """
    updated_output_filename: NewPath = generate_output_filename(
        general_settings, options
    )
    path: FilePath = (
        general_settings.PROCESSED_PATH
        / updated_output_filename
    ).resolve()
    save_dataframes_to_excel(transformed_data, path)
    format_worksheet(transformed_data, path, options)
    logging.info("Data has been loaded successfully")
    # Convert the file to base64
    file_name: str = updated_output_filename.name
    file_bytes: bytes = path.read_bytes()
    file_base64: str = base64.b64encode(file_bytes).decode("utf-8")
    file_base64 = f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{file_base64}"
    return file_name, file_base64

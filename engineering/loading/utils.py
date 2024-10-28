"""
A module for utils in the engineering.loading.formatting package.
"""

import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from pydantic import FilePath, NewPath

from config.settings import GeneralSettings
from schemas.request.options import Options


def generate_output_filename(
    settings: GeneralSettings,
    options: Options,
) -> NewPath:
    """
    Generate the output filename based on the current date.

    :param settings: The settings containing the base output filename
    :type settings: GeneralSettings
    :param options: The selected options
    :type options: dict[str, Any]
    :return: The updated output filename with the current month and year
    :rtype: NewPath
    """
    output_filename: NewPath = settings.OUTPUT_FILENAME
    today: datetime = datetime.now()
    base_name: str = output_filename.stem
    nodo: str = options.nodo  # type: ignore
    discount: str = options.discount_type  # type: ignore
    month: str = options.month  # type: ignore
    year: str = options.year  # type: ignore
    updated_output_filename: NewPath = Path(f"{base_name}_{nodo}_{discount}_{month}{year}_{today.strftime('%d_%m_%Y_%H_%M_%S')}.xlsx")
    return updated_output_filename

def save_dataframes_to_excel(
    data: dict[str, pd.DataFrame],
    path: FilePath,
) -> None:
    """
    Save dataframes into an Excel file.

    :param data: A dictionary with keys as sheet names and values as dataframes.
    :type data: Dict[str, pd.DataFrame]
    :param path: The file path where to save the Excel file
    :type path: FilePath
    :return: None
    :rtype: NoneType
    """
    with pd.ExcelWriter(path, engine="openpyxl") as excel_writer:
        for sheet_name, dataframe in data.items():
            if "Base" in sheet_name:
                dataframe.to_excel(excel_writer, sheet_name=sheet_name, startrow=2, index=False, header=False)
            if "Resumen" in sheet_name:
                dataframe.to_excel(excel_writer, sheet_name=sheet_name, index=False)

def save_dataframes_to_parquet(
    dataframes: dict[str, pd.DataFrame],
    general_settings: GeneralSettings,
) -> None:
    """
    Save dataframes into a JSON file.

    :param dataframes: A dictionary with keys as sheet names and values as dataframes.
    :type dataframes: Dict[str, pd.DataFrame]
    :param general_settings: The general settings required to save the dataframes
    :type general_settings: GeneralSettings
    """
    for name, dataframe in dataframes.items():
        file_path: str = f"{general_settings.RAW_PATH}/parquet/{name}.parquet"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        dataframe.to_parquet(file_path, engine="pyarrow", index=False)

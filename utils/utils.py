"""
A module for utils in the engineering.loading.formatting package.
"""
import io
import logging
from datetime import datetime
from pathlib import Path
from random import choices
from string import ascii_uppercase

import pandas as pd
from pydantic import NewPath, PositiveInt
from typing import Any

from config.settings import GeneralSettings
from core.decorators import benchmark, with_logging
from engineering.loading.formatting import format_worksheet

logger: logging.Logger = logging.getLogger(__name__)


def generate_output_filename(settings: GeneralSettings) -> NewPath:
    """
    Generate the output filename based on the current date.

    :param settings: The settings containing the base output filename
    :type settings: GeneralSettings
    :return: The updated output filename with the current month and year
    :rtype: NewPath
    """
    output_filename: NewPath = settings.OUTPUT_FILENAME
    today: datetime = datetime.now()
    base_name: str = output_filename.stem
    updated_output_filename: NewPath = Path(
        f"{base_name}{today.strftime("%d_%m_%Y_%H_%M_%S")}.xlsx"
    )
    logger.info(
        f"The name for the output file has been updated"
        f" {updated_output_filename}"
    )
    return updated_output_filename


@with_logging
@benchmark
def save_dataframes_to_excel(
    data_excel: dict[str, pd.DataFrame],
    data_additional: dict[str, pd.DataFrame],
    options: dict[str, Any],
) -> None:
    """
    Save dataframes into an Excel file.

    :param data_excel: A dictionary with keys as sheet names and values as dataframes.
    :type data_excel: dict[str, pd.DataFrame]
    :param data_additional: Additional data to be saved
    :type data_additional: dict[str, pd.DataFrame]
    :param options: The selected options
    :type options: dict[str, Any]
    :return: None
    :rtype: NoneType
    """
    output: io.BytesIO = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for sheet_name, dataframe in data_excel.items():
            dataframe.to_excel(writer, sheet_name=sheet_name, startrow=2, index=False, header=False)
            worksheet = writer.sheets[sheet_name]
            format_worksheet(worksheet, sheet_name, dataframe, data_additional, options)

    output.seek(0)
    logger.info(f"Data has been saved to Excel file")


def get_excel_column_letter(idx: PositiveInt) -> str:
    """
    Convert a column index (1-based) to an Excel column letter.

    :param idx: The column index to convert from an index to Excel column letter
    :type idx: PositiveInt
    :return: The column letter
    :rtype: str
    """
    column_letter: str = ""
    while idx > 0:
        idx, remainder = divmod(idx - 1, 26)
        column_letter = ascii_uppercase[remainder] + column_letter
    return column_letter

def get_cols_widths(dataframe: pd.DataFrame) -> list[int]:
    """
    Get the widths of the columns in the dataframe

    :param dataframe: The dataframe
    :type dataframe: pd.DataFrame
    :return: The widths of the columns
    :rtype: list[int]
    """
    # widths = [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]
    list_width = [max(len(str(val)) for val in dataframe[col].astype(str)) + 2 for col in dataframe.columns]
    return [w + 1 for w in list_width]

def trunc_number(number: int, decimals: int) -> float:
    """
    Truncate a number to a specific number of decimals

    :param number: The number to truncate
    :type number: int
    :param decimals: The number of decimals to keep
    :type decimals: int
    :return: The truncated number
    :rtype: float
    """
    factor: int = 10 ** decimals
    truncated_number: float = number.apply(lambda x: np.floor(x * factor) / factor) if isinstance(number, pd.Series) else np.floor(number * factor) / factor
    return truncated_number

def generate_random_color() -> str:
    """
    Generate a random color in hexadecimal format.

    :return: A random hexadecimal color string
    :rtype: str
    """
    return "".join(choices("0123456789ABCDEF", k=6))

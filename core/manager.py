"""
A module for persistence manager in the core package.
"""

from typing import Any, Type

import pandas as pd
from black import path_empty
from pandas.errors import EmptyDataError, ParserError
from pydantic import BaseModel, FilePath

from config.base_settings import BaseDataSettings
from schemas.validator import validate_dataframe


def load_file(
    settings: BaseDataSettings,
    model: Type[BaseModel],
    *args: tuple[Any, ...],
    **kwargs: dict[str, Any],
) -> pd.DataFrame:
    """
    Load the Excel file from the specified settings

    :param settings: The settings required to load
    :type settings: BaseDataSettings
    :param model: The Pydantic model to validate the data
    :type model: Type[BaseModel]
    :param args: Positional arguments to be passed to the function
    :type args: tuple[Any, ...]
    :param kwargs: Keyword arguments to be passed to the function
    :type kwargs: dict[str, Any]
    :return: The loaded dataframe from the given Excel file
    :rtype: pd.DataFrame
    """
    if not settings.FILENAME:
        raise ValueError("The filename must be specified")
    try:
        dataframe: pd.DataFrame = pd.read_excel(
            io=settings.FILENAME,
            sheet_name=settings.SHEET,
            header=settings.HEADER,
            usecols=settings.COLUMNS,
            *args,
            **kwargs,
        )
        # validate_dataframe(dataframe, model)
        return dataframe
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {settings.FILENAME}. Error: {e}")
    except EmptyDataError as e:
        raise EmptyDataError(f"No data found in the file: {settings.FILENAME}. Error: {e}")
    except ParserError as e:
        raise ParserError(f"Error parsing the file: {settings.FILENAME}. Error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while loading the file: {settings.FILENAME}. Error: {e}")

def load_parquet(
    settings: BaseDataSettings,
    *args: tuple[Any, ...],
    **kwargs: dict[str, Any],
) -> pd.DataFrame:
    """
    Load the JSON file from the specified settings

    :param settings: The settings required to load
    :type settings: BaseDataSettings
    :param args: Positional arguments to be passed to the function
    :type args: tuple[Any, ...]
    :param kwargs: Keyword arguments to be passed to the function
    :type kwargs: dict[str, Any]
    """
    if not settings.PARQUET_FILENAME:
        raise ValueError("The filename must be specified")
    try:
        dataframe: pd.DataFrame = pd.read_parquet(
            path=settings.PARQUET_FILENAME,
            *args,
            **kwargs,
        )
        return dataframe
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {settings.PARQUET_FILENAME}. Error: {e}")
    except EmptyDataError as e:
        raise EmptyDataError(f"No data found in the file: {settings.PARQUET_FILENAME}. Error: {e}")
    except ParserError as e:
        raise ParserError(f"Error parsing the file: {settings.PARQUET_FILENAME}. Error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while loading the file: {settings.PARQUET_FILENAME}. Error: {e}")

"""
A module for persistence manager in the core package.
"""

import logging
from typing import Any, Type

import pandas as pd
from pandas.errors import EmptyDataError, ParserError
from pydantic import BaseModel

from config.base_settings import BaseDataSettings
from core.decorators import benchmark
from schemas.validator import validate_dataframe
from schemas.demand import Demand

logger: logging.Logger = logging.getLogger(__name__)


@benchmark
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
        logger.error("The filename must be specified.")
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
        dataframe = dataframe.where(pd.notnull(dataframe), None)
        logger.info(f"File {settings.FILENAME.stem} loaded successfully.")
        # TODO: Handle the data validation process for each schema.
        # If model is Demand, use the dynamic validation
        if model == Demand:
            validate_dataframe(dataframe, model, dynamic=True)
        else:
            # Validate the dataframe using the specified static model schema
            validate_dataframe(dataframe, model)
        return dataframe
    except FileNotFoundError as e:
        logger.error(f"File not found: {settings.FILENAME}. Error: {e}")
        raise FileNotFoundError(f"File not found: {settings.FILENAME}. Error: {e}")
    except EmptyDataError as e:
        logger.error(
            f"No data found in the file: {settings.FILENAME}. Error: {e}"
        )
        raise EmptyDataError(f"No data found in the file: {settings.FILENAME}. Error: {e}")
    except ParserError as e:
        logger.error(f"Error parsing the file: {settings.FILENAME}. Error: {e}")
        raise ParserError(f"Error parsing the file: {settings.FILENAME}. Error: {e}")
    except Exception as e:
        logger.error(
            f"An unexpected error occurred while loading the file:"
            f" {settings.FILENAME}. Error: {e}"
        )
        raise Exception(
            f"An unexpected error occurred while loading the file: {settings.FILENAME}. Error: {e}"
        )

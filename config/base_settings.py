"""
A module for base settings in the config package.
"""

import logging
from datetime import datetime
from pathlib import Path

from pydantic import DirectoryPath, FilePath, NonNegativeInt, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings

logger: logging.Logger = logging.getLogger(__name__)


class BasePathSettings(BaseSettings):
    """Base class for settings for paths."""

    RAW_PATH: DirectoryPath

    @field_validator("*", mode="before", check_fields=True)
    def validate_filenames(
        cls, v: str, info: FieldValidationInfo
    ) -> FilePath | str:
        """
        Validator to ensure filename fields end with '.xlsx'

        :param v: The name of the field to validate
        :type v: str
        :param info: The full information about the fields from the class
        :type info: FieldValidationInfo
        :return: The validated class attribute
        :rtype: FilePath | str
        """
        if info.field_name is None:
            logging.error("info.config cannot be None")
            raise ValueError("info.config cannot be None")
        if info.field_name == "FILENAME":
            if not v.endswith(".xlsx") and not v.endswith(".xlsm"):
                logging.error(
                    f"{info.field_name} must be a string ending with '.xlsx' "
                    f"or '.xlsm'"
                )
                raise ValueError(
                    f"{info.field_name} must be a string ending with '.xlsx' "
                    f"or '.xlsm'"
                )
            raw_path_str: str | None = info.data.get("RAW_PATH")
            if not raw_path_str:
                logging.error("Missing RAW_PATH")
                raise ValueError("Missing RAW_PATH")
            raw_path: DirectoryPath = Path(raw_path_str)
            today: datetime = datetime.now()
            year: str = today.strftime("%Y")
            # month: str = str(int(today.strftime("%m")) - 1)
            month: str = str(int(today.strftime("%m")))
            return (raw_path / year / month / v).resolve()
        return v


class BaseDataSettings(BasePathSettings):
    """
    Base data class for settings with common filename, sheet, header,
    and columns.
    """

    FILENAME: FilePath
    SHEET: str
    COLUMNS: list[str]
    HEADER: NonNegativeInt | None = 0

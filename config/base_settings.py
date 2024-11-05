"""
A module for base settings in the config package.
"""

from pathlib import Path

from pydantic import DirectoryPath, FilePath, NewPath, NonNegativeInt, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings


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
            raise ValueError("info.config cannot be None")
        if info.field_name == "FILENAME" or info.field_name == "PARQUET_FILENAME":
            if not v.endswith(".xlsx") and not v.endswith(".parquet"):
                raise ValueError(
                    f"{info.field_name} must be a string ending with '.xlsx' "
                    f"or '.parquet'"
                )
            raw_path_str: str | None = info.data.get("RAW_PATH")
            if not raw_path_str:
                raise ValueError("Missing RAW_PATH")
            raw_path: DirectoryPath = Path(raw_path_str)
            if info.field_name == "FILENAME":
                return (raw_path / v).resolve()
            elif info.field_name == "PARQUET_FILENAME":
                parquet_dir: str = "parquet"
                return (raw_path / parquet_dir / v).resolve()
        return v


class BaseDataSettings(BasePathSettings):
    """
    Base data class for settings with common filename, sheet, header,
    and columns.
    """

    FILENAME: NewPath | FilePath
    PARQUET_FILENAME: NewPath | FilePath
    SHEET: str
    COLUMNS: list[str]
    HEADER: NonNegativeInt | None = 0

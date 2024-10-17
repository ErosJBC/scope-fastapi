"""
A module for settings in the config package.
"""

import logging
from datetime import datetime
from functools import lru_cache

from pydantic import (
    DirectoryPath,
    NewPath,
    PositiveFloat,
    PositiveInt,
    field_validator,
)
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.base_settings import BaseDataSettings

logger: logging.Logger = logging.getLogger(__name__)


class ClientSettings(BaseDataSettings):
    """Settings for client data processing"""

    model_config = SettingsConfigDict(
        env_file=".env.clients",
    )

    COD_PAIS: list[str]
    GERENCIA: list[str]
    LIMITE_INF_ZENT_S4: PositiveInt
    LIMITE_SUP_ZNJE_CRM: PositiveInt


class SKUSettings(BaseDataSettings):
    """Settings for SKU data processing"""

    model_config = SettingsConfigDict(env_file=".env.sku")

    CATEGORIA: str
    STATUS_S4: str


class DemandSettings(BaseDataSettings):
    """Settings for demand data processing"""

    model_config = SettingsConfigDict(env_file=".env.demand")

    REGION: str
    PAISES: list[str]
    GERENCIA: list[str]
    CATEGORIA: str
    DATO: str

    @field_validator(
        "DATO",
        mode="after",
    )
    def validate_dato(cls, v: str, info: FieldValidationInfo) -> str:
        """
        Validator to ensure filename fields end with '.xlsx'

        :param v: The name of the field to validate
        :type v: str
        :param info: The full information about the fields from the class
        :type info: FieldValidationInfo
        :return: The validated class attribute
        :rtype: str
        """
        if info.field_name is None:
            logging.error("info.config cannot be None")
            raise ValueError("info.config cannot be None")
        today: datetime = datetime.now()
        month: str = today.strftime("%b").upper()
        year: int = int(today.strftime("%y"))
        full_year: int = int(today.strftime("%Y"))
        data: str = f"PY{month}{year}({full_year})"
        # data: set[str] = {f"PY{month}{year}({full_year})", f"PY{month}{year}({full_year + 1})"}
        return data


class SalesSettings(BaseDataSettings):
    """Settings for sales data processing"""

    model_config = SettingsConfigDict(env_file=".env.sales")

    BASE_NAME: str = "Archivo Ventas Maestro FJM22"
    FAMILIA: str
    COLUMNS_TO_DROP: list[str]
    FILTER_COLS: list[str]
    CASH_PAYMENT_CONDITIONS: list[str]

    # @field_validator(
    #     "FILENAME",
    #     mode="after",
    # )
    # def generate_filename(cls, v: str | None, info: FieldValidationInfo) -> str:
    #     """
    #     Validator to dynamically generate the FILENAME with the current month
    #      and year.
    #
    #     :param v: The filename value to validate (if provided, otherwise None)
    #     :type v: str | None
    #     :param info: Field validation context
    #     :type info: FieldValidationInfo
    #     :return: The dynamically generated filename with current month and year
    #     :rtype: str
    #     """
    #     if info.field_name is None:
    #         logging.error("info.config cannot be None")
    #         raise ValueError("info.config cannot be None")
    #     today: datetime = datetime.now()
    #     month: str = today.strftime("%b").upper()
    #     year: str = today.strftime("%Y")
    #     if info.data.get("CONTACT_NAME"):
    #         filename: str = f"{info.data.get("BASE_NAME")} {month} {year}.xlsx"
    #         return filename
    #     return str(info.data.get("BASE_NAME"))


class CashSettings(BaseDataSettings):
    """Settings for cash sales data processing"""

    model_config = SettingsConfigDict(env_file=".env.cash")

    # FILENAME: FilePath = Path("discount_project_ago_2024.xlsx")
    #
    # @field_validator("FILENAME", mode="before")
    # def generate_filename(
    #     cls, v: str | None, info: FieldValidationInfo
    # ) -> FilePath:
    #     """
    #     Validator to dynamically generate the FILENAME with the last month's
    #      name and year.
    #
    #     :param v: The filename value to validate (if provided, otherwise None)
    #     :type v: str | None
    #     :param info: Field validation context
    #     :type info: FieldValidationInfo
    #     :return: The dynamically generated filename with last month's name and
    #      year
    #     :rtype: FilePath
    #     """
    #     if info.field_name is None:
    #         logging.error("info.config cannot be None")
    #         raise ValueError("info.config cannot be None")
    #     last_month: datetime = datetime.now() - relativedelta(months=1)
    #     last_month_name: str = last_month.strftime("%b").lower()
    #     year: str = last_month.strftime("%Y")
    #     if info.data.get("FILENAME"):
    #         filename: FilePath = Path(
    #             f"{info.data.get("FILENAME")}_{last_month_name}_"
    #             f"{year}.xlsx"
    #         )
    #         return filename
    #     return Path(info.data.get("FILENAME"))


class PriceSettings(BaseDataSettings):
    """Settings for prices data processing"""

    model_config = SettingsConfigDict(env_file=".env.prices")

    FAMILIA: str
    RAZON_SACO_10KG_ORI: PositiveFloat
    RAZON_SACO_25KG: PositiveFloat


class BasePriceSettings(BaseDataSettings):
    """Settings for base prices data processing"""

    model_config = SettingsConfigDict(env_file=".env.base_prices")


class GeneralSettings(BaseSettings):
    """General settings for common configurations"""

    RAW_PATH: DirectoryPath
    PROCESSED_PATH: DirectoryPath
    OUTPUT_FILENAME: NewPath

    model_config = SettingsConfigDict(env_file=".env")


class Settings(BaseSettings):
    """Main settings class that encapsulates all specific settings"""

    general: GeneralSettings = GeneralSettings()  # type: ignore
    clients: ClientSettings = ClientSettings(  # type: ignore
        RAW_PATH=general.RAW_PATH
    )
    skus: SKUSettings = SKUSettings(RAW_PATH=general.RAW_PATH)  # type: ignore
    demand: DemandSettings = DemandSettings(  # type: ignore
        RAW_PATH=general.RAW_PATH
    )
    cash: CashSettings = CashSettings(RAW_PATH=general.RAW_PATH)  # type: ignore
    sales: SalesSettings = SalesSettings(  # type: ignore
        RAW_PATH=general.RAW_PATH
    )
    prices: PriceSettings = PriceSettings(  # type: ignore
        RAW_PATH=general.RAW_PATH
    )
    base_prices: BasePriceSettings = BasePriceSettings(  # type: ignore
        RAW_PATH=general.RAW_PATH
    )


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings

    :return: The settings instance
    :rtype: Settings
    """
    return Settings()


settings: Settings = get_settings()

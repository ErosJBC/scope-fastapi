"""
A module for settings in the config package.
"""

from functools import lru_cache

from pydantic import (
    DirectoryPath,
    NewPath
)
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.base_settings import BaseDataSettings


class BinnacleSettings(BaseDataSettings):
    """Settings for binnacle data processing"""

    model_config = SettingsConfigDict(env_file=".env.binnacle")

    STATUS: str
    VIA: str
    RENAME_COLUMNS: list[str]


class ClientSettings(BaseDataSettings):
    """Settings for clients data processing"""

    model_config = SettingsConfigDict(env_file=".env.client")

    DES_PAIS: list[str]
    FILTER_COLUMNS: list[str]


class PriceSettings(BaseDataSettings):
    """Settings for prices data processing"""

    model_config = SettingsConfigDict(env_file=".env.price")

    CONSIDER: str
    STATUS_SKU: str
    RENAME_COLUMNS: list[str]


class SaleSettings(BaseDataSettings):
    """Settings for sales data processing"""

    model_config = SettingsConfigDict(env_file=".env.sale")

    RENAME_COLUMNS: list[str]
    MERGE_COLUMNS: list[str]


class SellOutSettings(BaseDataSettings):
    """Settings for sellout data processing"""

    model_config = SettingsConfigDict(env_file=".env.sellout")

    TYPE: str
    RENAME_COLUMNS: list[str]


class GeneralSettings(BaseSettings):
    """General settings for common configurations"""

    RAW_PATH: DirectoryPath
    PROCESSED_PATH: DirectoryPath
    OUTPUT_FILENAME: NewPath

    model_config = SettingsConfigDict(env_file=".env")


class Settings(BaseSettings):
    """Main settings class that encapsulates all specific settings"""

    general: GeneralSettings = GeneralSettings()  # type: ignore
    binnacle: BinnacleSettings = BinnacleSettings(  # type: ignore
        RAW_PATH=general.RAW_PATH
    )
    clients: ClientSettings = ClientSettings(  # type: ignore
        RAW_PATH=general.RAW_PATH
    )
    prices: PriceSettings = PriceSettings(  # type: ignore
        RAW_PATH=general.RAW_PATH
    )
    sales: SaleSettings = SaleSettings(  # type: ignore
        RAW_PATH=general.RAW_PATH
    )
    sellout: SellOutSettings = SellOutSettings(  # type: ignore
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

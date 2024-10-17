"""
A module for init settings in the config package.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Init Settings class based on Pydantic Base Settings"""

    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="allow",
    )

    APP_NAME: str = "S.C.O.P.E."
    APP_DESCRIPTION: str = "SCOPE application developed in Dash framework"


@lru_cache
def get_app_settings() -> AppSettings:
    """
    Get the cached init settings

    :return: The init settings instance
    :rtype: InitSettings
    """
    return AppSettings()


app_settings: AppSettings = get_app_settings()

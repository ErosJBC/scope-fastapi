"""
A module for logging setup in the core package.
"""

import logging
import os
from datetime import datetime

from pydantic import PositiveInt

from config.init_settings import InitSettings


def _setup_console_handler(
    logger: logging.Logger, log_level: PositiveInt
) -> None:
    """
    Configure a console handler for the given logger

    :param logger: The logger instance to set up a console handler for
    :type logger: logging.Logger
    :param log_level: The log level for the console handler
    :type log_level: PositiveInt
    :return: None
    :rtype: NoneType
    """
    stream: logging.StreamHandler = logging.StreamHandler()  # type: ignore
    stream.setLevel(log_level)
    logger.addHandler(stream)


def _create_logs_folder(project_name: str) -> str:
    """
    Create a logs folder if it doesn't already exist

    :param project_name: The project name to validate logs folder creation
    :type project_name: str
    :return: The path to the logs folder
    :rtype: str
    """
    project_root: str = os.path.dirname(os.path.abspath(__file__))
    while os.path.basename(project_root) != project_name:
        project_root = os.path.dirname(project_root)
    logs_folder_path: str = f"{project_root}/logs"
    if not os.path.exists(logs_folder_path):
        os.makedirs(logs_folder_path, exist_ok=True)
    return logs_folder_path


def _build_log_filename(file_date_format: str) -> str:
    """
    Create a log filename using the current date and configured date
     format.

    :param file_date_format: The format of the log filename using date format
    :type file_date_format: str
    :return: The filename for the log file
    :rtype: str
    """
    return f"log-{datetime.now().strftime(file_date_format)}.log"


def _configure_file_handler(
    log_filename: str, log_level: PositiveInt, init_settings: InitSettings
) -> logging.FileHandler:
    """
    Configure a file handler with the given filename and log level

    :param log_filename: The filename for the log file
    :type log_filename: str
    :param log_level: The log level for the file handler
    :type log_level: PositiveInt
    :param init_settings: Dependency method for cached init setting object
    :type init_settings: InitSettings
    :return: A configured file handler
    :rtype: logging.FileHandle
    """
    formatter: logging.Formatter = logging.Formatter(
        init_settings.LOG_FORMAT, init_settings.DATETIME_FORMAT
    )
    file_handler: logging.FileHandler = logging.FileHandler(log_filename)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    return file_handler


def _setup_file_handler(
    logger: logging.Logger,
    log_level: PositiveInt,
    init_settings: InitSettings,
) -> None:
    """
    Configure a file handler for the given logger

    :param logger: The logger instance to set up a file handler for
    :type logger: logging.Logger
    :param log_level: The log level for the file handler
    :type log_level: PositiveInt
    :param init_settings: Dependency method for cached init setting object
    :type init_settings: InitSettings
    :return: None
    :rtype: NoneType
    """
    logs_folder_path: str = _create_logs_folder(init_settings.PROJECT_NAME)
    log_filename: str = _build_log_filename(init_settings.FILE_DATE_FORMAT)
    filename_path: str = f"{logs_folder_path}/{log_filename}"
    file_handler: logging.FileHandler = _configure_file_handler(
        filename_path, log_level, init_settings
    )
    logger.addHandler(file_handler)
    file_handler.flush()


def setup_logging(
    init_settings: InitSettings,
    log_level: PositiveInt = logging.DEBUG,
) -> None:
    """
    Initialize logging for the application

    :param init_settings: Dependency method for cached init setting object
    :type init_settings: InitSettings
    :param log_level: The log level to use for the application.
     Defaults to DEBUG
    :type log_level: PositiveInt
    :return: None
    :rtype: NoneType
    """
    logger: logging.Logger = logging.getLogger()
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(log_level)
    _setup_console_handler(logger, log_level)
    _setup_file_handler(logger, log_level, init_settings)

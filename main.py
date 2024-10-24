"""
The main script to run the project
"""

import logging

import uvicorn

from config.settings import settings
from engineering.engineering import run_load_data

logger: logging.Logger = logging.getLogger(__name__)


def main() -> None:
    """
    The main function to run the project

    :return: None
    :rtype: NoneType
    """
    logger.info("Starting the data loading process.")
    try:
        run_load_data(settings)
        logger.info("Data loaded successfully")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()

"""
The main script to run the project
"""

import logging

import uvicorn

logger: logging.Logger = logging.getLogger(__name__)


def main() -> None:
    """
    The main function to run the project

    :return: None
    :rtype: NoneType
    """
    logger.info("Starting the project")

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()

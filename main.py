"""
The main script to run the project
"""

import logging

from views.view import app


logger: logging.Logger = logging.getLogger(__name__)


def main() -> None:
    """
    Execute the dash app.
    Sets up the necessary configurations and runs the dash app.
    :return: None
    :rtype: NoneType
    """
    logger.info("Running main method")
    app.run_server(debug=True)
    logging.info("Main method has been run successfully")


if __name__ == "__main__":
    main()

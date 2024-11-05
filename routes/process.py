"""
This file contains the route for processing the data.
"""

import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from config.settings import settings
from engineering.engineering import run_load_data

processRouter = APIRouter()

logger: logging.Logger = logging.getLogger(__name__)


@processRouter.post("/process", tags=["Process Data"], status_code=200)
async def process_data() -> JSONResponse:
    """
    Process the Excel files.

    :return: The files loaded successfully
    :rtype: JSONResponse
    """
    try:
        run_load_data(settings)
        logger.info("Files processed successfully")
        return JSONResponse(content={"message": "Files processed successfully"})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return JSONResponse(content={"message": f"An error occurred: {e}"}, status_code=500)

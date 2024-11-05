"""
This file contains the route for loading the data.
"""

import logging

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from engineering.utils import load_excel_files

loadRouter = APIRouter()

logger: logging.Logger = logging.getLogger(__name__)


@loadRouter.post("/load", tags=["Load Data"], status_code=200)
async def load_data(files: list[UploadFile] = File(...)) -> JSONResponse:
    """
    Load the Excel file to be processed.

    :param files: The files to be loaded
    :type files: list[UploadFile]
    :return: The files loaded successfully
    :rtype: JSONResponse
    """
    try:
        logger.info("Loading data")
        load_excel_files(files)
        logger.info("Files loaded successfully")
        return JSONResponse(content={"message": "Files loaded successfully"})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return JSONResponse(content={"message": f"An error occurred: {e}"}, status_code=500)

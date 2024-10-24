"""
This module contains the routes for filtering the data based on the options provided.
"""

import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from engineering.utils import generate_filtered_options
from schemas.request.options import Options

filterRouter = APIRouter()

logger: logging.Logger = logging.getLogger(__name__)


@filterRouter.get("/filter", tags=["Filter Options for Data"])
async def filter_options(options: Options = Depends()) -> JSONResponse:
    try:
        filtered_options = generate_filtered_options(options)
        logger.info("Filtering data")
        return JSONResponse(content={"message": "Filtered options got successfully", "options": filtered_options})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return JSONResponse(content={"message": f"An error occurred: {e}"}, status_code=500)

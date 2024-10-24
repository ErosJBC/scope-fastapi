"""
This file contains the route for generating the Excel file.
"""

import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from engineering.utils import generate_excel_file
from schemas.request.options import Options

generateRouter = APIRouter()

logger: logging.Logger = logging.getLogger(__name__)


@generateRouter.post("/generate", tags=["Generate Data"])
async def generate_data(options: Options) -> JSONResponse:
    try:
        generated_file = generate_excel_file(options)
        logger.info("Generating data")
        return JSONResponse(content={"message": "File generated successfully", "file": generated_file})
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return JSONResponse(content={"message": f"An error occurred: {e}"}, status_code=500)

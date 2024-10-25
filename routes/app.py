"""
This module contains the init router for the FastAPI application.
"""

import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

initRouter = APIRouter()

logger: logging.Logger = logging.getLogger(__name__)


@initRouter.get("/", tags=["App"], status_code=200)
async def init_root() -> JSONResponse:
    """
    Welcome message for the application.

    :return: The welcome message
    :rtype: JSONResponse
    """
    return JSONResponse(content={"message": "Welcome to this fantastic app!"})

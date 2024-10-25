"""
This module contains the routes for the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from routes.app import initRouter
from routes.filter import filterRouter
from routes.generate import generateRouter


def load_routes(init_app: FastAPI) -> None:
    """
    Load the routes into the FastAPI application

    :param init_app: The FastAPI application
    :type init_app: FastAPI
    :return: None
    :rtype: NoneType
    """
    init_app.include_router(initRouter)
    init_app.include_router(filterRouter)
    init_app.include_router(generateRouter)



from fastapi import FastAPI

from routes.filter import filterRouter
from routes.generate import generateRouter


def load_routes(app: FastAPI) -> None:
    """
    Load the routes into the FastAPI application

    :param app: The FastAPI application
    :type app: FastAPI
    :return: None
    :rtype: NoneType
    """
    app.include_router(filterRouter)
    app.include_router(generateRouter)

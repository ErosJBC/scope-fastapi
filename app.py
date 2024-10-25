"""
This module is the entry point of the FastAPI application.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.init_settings import init_settings, InitSettings
from routes.routes import load_routes

logger: logging.Logger = logging.getLogger(__name__)


def create_app(settings: InitSettings) -> FastAPI:
    """
    Create the FastAPI application

    :return: The FastAPI application
    """
    init_app = FastAPI(
        title=settings.APP_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
    )
    # Allow CORS for the application
    init_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    load_routes(init_app)
    return init_app

app = create_app(init_settings)
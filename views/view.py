"""
A module for home view in the view package.
"""

from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from config.app_settings import app_settings, AppSettings
from views.home.home import home_layout


def init_app(settings: AppSettings) -> Dash:
    """
    Initialize the application
    :return: The initialized application
    :rtype: None
    """
    view = Dash(
        __name__,
        external_stylesheets=[BOOTSTRAP],
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
    )
    view.layout = home_layout
    return view

app = init_app(app_settings)

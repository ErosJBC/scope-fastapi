"""
A component module for logo in the components package.
"""
from dash.html import Img
from dash_bootstrap_components import Col
from pydantic import FilePath
from utils.image.image import encode_image

class LogoSettings:
    def __init__(self, logo_path: str, width: str = "100%", max_width: str = "300px", class_name: str = "text-center"):
        self.logo_path = FilePath(logo_path)
        self.width = width
        self.max_width = max_width
        self.class_name = class_name

class Logo(LogoSettings):
    """
    A class used to create a logo based on the settings provided
    """
    def __init__(self, logo_path: str, width: str = "100%", max_width: str = "300px", class_name: str = "text-center"):
        super().__init__(logo_path, width, max_width, class_name)
        self.logo = None

    def __call__(self) -> Col:
        """
        Create a logo based on the settings provided
        :return: A logo based on the settings provided
        :rtype: Col
        """
        self.logo = self.create_logo()
        return self.logo

    def create_logo(self) -> Col:
        """
        Create a logo with the settings provided
        :return: A logo with the settings provided
        :rtype: Col
        """
        logo = Col(
            Img(
                src=encode_image(self.logo_path),
                style={
                    "width": self.width,
                    "max-width": self.max_width,
                    "display": "block",
                    "margin-left": "auto",
                    "margin-right": "auto",
                },
            ),
            xs=12, sm=12, md=4,
            className=self.class_name
        )
        return logo

"""
A component module for button action in the components package.
"""
from typing import Any
from dash.html import Button, A

class ButtonActionSettings:
    """
    A class used to store the settings for a button or a link
    """
    def __init__(self, button_type: str, title: str, **kwargs: Any) -> None:
        self.type = button_type
        self.title = title
        self.kwargs = kwargs


class ButtonAction(ButtonActionSettings):
    """
    A class used to create a button or a link based on the settings provided
    """
    def __init__(self, button_type: str, title: str, **kwargs: Any) -> None:
        super().__init__(button_type, title, **kwargs)
        self.button_action = None

    def __call__(self) -> Any:
        """
        Create a button or a link based on the settings provided
        :return: A button or a link based on the settings provided
        :rtype: Button or A
        """
        if self.type == "button":
            self.button_action = self.create_button()
        elif self.type == "link":
            self.button_action =  self.create_link()
        return self.button_action

    def create_button(self) -> Button:
        """
        Create a button with the settings provided
        :return: A button with the settings provided
        :rtype: Button
        """
        button = Button(self.title, **self.kwargs)
        return button

    def create_link(self) -> A:
        """
        Create a link with the settings provided
        :return: A link with the settings provided
        :rtype: A
        """
        anchor = A(self.title, **self.kwargs)
        return anchor

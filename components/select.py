"""
A component module for select in the components package.
"""
from typing import Any, Union
from dash.dcc import Dropdown
from dash_bootstrap_components import Label

class SelectSettings:
    """
    A class used to store the settings for a button or a link
    """
    def __init__(self, label: Any, dropdown: Any) -> None:
        self.label = label
        self.dropdown = dropdown


class Select(SelectSettings):
    """
    A class used to create a select based on the settings provided
    """
    def __init__(self, label: Any, dropdown: Any) -> None:
        super().__init__(label, dropdown)
        self.select: list[Union[Label, Dropdown]] = []

    def __call__(self) -> list[Union[Label, Dropdown]]:
        """
        Create a select based on the settings provided
        :return: A select based on the settings provided
        :rtype: Div
        """
        self.select = self.create_select()
        return self.select

    def create_select(self) -> list[Union[Label, Dropdown]]:
        """
        Create a select with the settings provided
        :return: A select with the settings provided
        :rtype: Div
        """
        select = [Label(**self.label), Dropdown(**self.dropdown)]
        return select

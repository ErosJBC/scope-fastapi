"""
A component module for title in the components package.
"""
from typing import Any
from dash.html import H1, H2, H3, H4, H5, H6

class TitleSettings:
    """
    A class used to store the settings for a title
    """
    def __init__(self, h_type: str, text: str, **kwargs: Any) -> None:
        self.header = h_type
        self.text = text
        self.kwargs = kwargs


class Title(TitleSettings):
    """
    A class used to create a title based on the settings provided
    """
    def __init__(self, h_type: str, text: str, **kwargs: Any) -> None:
        super().__init__(h_type, text, **kwargs)
        self.title = None

    def __call__(self) -> H1 | H2 | H3 | H4 | H5 | H6:
        """
        Create a title based on the settings provided
        :return: A title based on the settings provided
        :rtype: H1 | H2 | H3 | H4 | H5 | H6
        """
        if self.header == "h1":
            self.title = self.create_title_h1()
        elif self.header == "h2":
            self.title = self.create_title_h2()
        elif self.header == "h3":
            self.title = self.create_title_h3()
        elif self.header == "h4":
            self.title = self.create_title_h4()
        elif self.header == "h5":
            self.title = self.create_title_h5()
        elif self.header == "h6":
            self.title = self.create_title_h6()
        else:
            raise ValueError(f"Unsupported header type: {self.header}")
        return self.title

    def create_title_h1(self) -> H1:
        """
        Create a h1 title with the settings provided
        :return: A h1 title with the settings provided
        :rtype: H1
        """
        title = H1(self.text, **self.kwargs)
        return title

    def create_title_h2(self) -> H2:
        """
        Create a h2 title with the settings provided
        :return: A h2 title with the settings provided
        :rtype: H2
        """
        title = H2(self.text, **self.kwargs)
        return title

    def create_title_h3(self) -> H3:
        """
        Create a h3 title with the settings provided
        :return: A h3 title with the settings provided
        :rtype: H3
        """
        title = H3(self.text, **self.kwargs)
        return title

    def create_title_h4(self) -> H4:
        """
        Create a h4 title with the settings provided
        :return: A h4 title with the settings provided
        :rtype: H4
        """
        title = H4(self.text, **self.kwargs)
        return title

    def create_title_h5(self) -> H5:
        """
        Create a h5 title with the settings provided
        :return: A h5 title with the settings provided
        :rtype: H5
        """
        title = H5(self.text, **self.kwargs)
        return title

    def create_title_h6(self) -> H6:
        """
        Create a h6 title with the settings provided
        :return: A h6 title with the settings provided
        :rtype: H6
        """
        title = H6(self.text, **self.kwargs)
        return title

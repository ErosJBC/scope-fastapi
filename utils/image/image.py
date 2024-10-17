"""
A module for image in the utils.image.image package.
"""

import base64

from pydantic import FilePath

def encode_image(image_path: FilePath) -> str:
    """
    Encode VTP image interface to base64
    :param image_path:
    :return: str
    """
    with open(image_path, "rb") as image_file:
        image_encode: str = base64.b64encode(image_file.read()).decode("utf-8")

    return f"data:image/jpg;base64,{image_encode}"
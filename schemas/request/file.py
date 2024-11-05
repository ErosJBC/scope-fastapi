"""
This module contains the schema for the file request.
"""

from pydantic import BaseModel, Field


class File(BaseModel):
    """File for loading data"""
    filename: str = Field(
        ...,
        title="Filename",
        description="The filename",
    )
    file_base64: str = Field(
        ...,
        title="File in base64",
        description="The file in base64",
    )

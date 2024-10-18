"""
A module for validator in the schemas package.
"""

from typing import Any, Type

import pandas as pd
from pydantic import BaseModel, Field, ValidationError, create_model


def validate_dataframe(
    dataframe: pd.DataFrame,
    model: Type[BaseModel]
) -> list[BaseModel]:
    """
    Validate a DataFrame against a Pydantic model.

    :param dataframe: The DataFrame to validate
    :type dataframe: pd.DataFrame
    :param model: The Pydantic model to validate against
    :type model: Type[BaseModel]
    :return: A list of validated Pydantic model instances
    :rtype: list[BaseModel]
    :raises ValidationError: If the DataFrame does not match the model schema
    """
    data_dict: list[dict[str, Any]] = dataframe.to_dict(orient="records")
    try:
        validated_data: list[BaseModel] = [model(**item) for item in data_dict]
        return validated_data
    except ValidationError as e:
        raise ValidationError(f"Data validation error: {e}")

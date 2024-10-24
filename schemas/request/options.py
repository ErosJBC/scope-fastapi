"""
This module contains the schema for the options request.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Options(BaseModel):
    """Options for filtering data"""
    liquidation: Optional[str] = Field(
        None,
        title="Liquidation",
        description="The selected liquidation",
    )
    nodo: Optional[str] = Field(
        None,
        title="Nodo",
        description="The selected nodo",
    )
    discount_type: Optional[str] = Field(
        None,
        title="Discount Type",
        description="The selected discount type",
    )
    year: Optional[str] = Field(
        None,
        title="Year",
        description="The selected year",
    )
    month: Optional[str] = Field(
        None,
        title="Month",
        description="The selected month",
    )

"""
A module for price in the schemas package.
"""

from pydantic import BaseModel, Field, PositiveInt


class Price(BaseModel):
    """Price table representation for data validation from its Excel file"""

    consider: str | float | None = Field(
        None,
        alias="Considerar",
        title="Consideration",
        description="Indicates whether this price should be considered in calculations."
    )
    sku_status: str | float | None = Field(
        None,
        alias="Status SKU",
        title="SKU Status",
        description="Represents the current status of the SKU, indicating its availability or condition."
    )
    s4_node: float | None = Field(
        None,
        alias="Nodo S4",
        title="S4 Node",
        description="The identifier for the S4 Node associated with this price entry."
    )
    material: float | None = Field(
        None,
        alias="material",
        title="Material",
        description="The type of material related to this price, providing context for its classification."
    )
    base_price: float = Field(
        ...,
        alias="P. Base",
        title="Base Price",
        description="The initial price before any discounts or adjustments are applied."
    )
    total_discount: float = Field(
        ...,
        alias="Total Dscto",
        title="Total Discount",
        description="The cumulative discount applied to the base price, impacting the final cost."
    )

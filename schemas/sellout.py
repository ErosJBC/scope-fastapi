"""
A module for sellout in the schemas package.
"""

from pydantic import BaseModel, Field, PastDate, NonPositiveInt, PositiveInt


class SellOut(BaseModel):
    """Sell Out table representation for data validation from its Excel file"""

    type: str = Field(
        ...,
        alias="Tipo",
        title="Type",
        description="Indicates the type of the sellout transaction, categorizing the nature of the sale."
    )
    date: PastDate = Field(
        ...,
        alias="Fecha",
        title="Date",
        description="The date when the transaction took place; must be in the past."
    )
    receipt_number: str | float | None = Field(
        None,
        alias="Nro_Comprobante",
        title="Receipt Number",
        description="The unique identifier for the receipt associated with the transaction."
    )
    payment_condition_type: str | float | None = Field(
        None,
        alias="Tip_Condicion_Pago",
        title="Payment Condition Type",
        description="Specifies the type of payment condition applicable to this transaction."
    )
    node_code: float | None = Field(
        None,
        alias="Cod_Nodo",
        title="Node Code",
        description="The code identifying the node involved in this sale."
    )
    distributor: str = Field(
        ...,
        alias="Distribuidor",
        title="Distributor",
        description="The name of the distributor responsible for the sellout."
    )
    cod_zdes: float | str | None = Field(
        None,
        alias="COD_ZDES",
        title="ZDES Code",
        description="The code representing the ZDES associated with this transaction."
    )
    des_zdes: str | float | None = Field(
        None,
        alias="DES_ZDES",
        title="ZDES Description",
        description="A description of the ZDES for better understanding of the entry."
    )
    unified_item: PositiveInt = Field(
        ...,
        alias="Item Unificado",
        title="Unified Item",
        description="The identifier for the unified item being sold."
    )
    short_description: str = Field(
        ...,
        alias="Descripcion Abreviada",
        title="Short Description",
        description="A brief description of the item for quick reference."
    )
    quantity: float | None = Field(
        None,
        alias="CANTIDAD",
        title="Quantity Sold",
        description="The total quantity of items sold in this transaction."
    )
    ton: float | None = Field(
        None,
        alias="Ton",
        title="Tons Sold",
        description="The total weight of items sold measured in tons."
    )
    category: NonPositiveInt | str = Field(
        ...,
        alias="Categoria",
        title="Category",
        description="The category classification of the item sold, providing context for its type."
    )
    stage: NonPositiveInt | str = Field(
        ...,
        alias="Etapa",
        title="Stage",
        description="The current stage of the sellout process for this transaction."
    )

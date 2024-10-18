"""
A module for binnacle in the schemas package.
"""

from pydantic import BaseModel, Field, PositiveInt

class Binnacle(BaseModel):
    """Binnacle table representation for data validation from its Excel file"""

    status: str = Field(
        ...,
        alias="Status",
        title="Status",
        description="The current status of the binnacle entry, indicating its state in the process."
    )
    via: str = Field(
        ...,
        alias="Vía",
        title="Via",
        description="The channel or route through which the binnacle entry was processed."
    )
    client_type: str = Field(
        ...,
        alias="Cliente Tipo",
        title="Client Type",
        description="Indicates the category or type of client involved in the transaction."
    )
    node_code: PositiveInt = Field(
        ...,
        alias="Cod Nodo",
        title="Node Code",
        description="A unique identifier for the node related to the binnacle entry."
    )
    node: str = Field(
        ...,
        alias="Nodo",
        title="Node",
        description="The name of the node, providing additional context to its identifier."
    )
    cod_zdes: float | str | None = Field(
        None,
        alias="COD_ZDES",
        title="ZDES Code",
        description="The code representing the ZDES related to this entry, essential for tracking."
    )
    cod_zdem: float | str | None = Field(
        None,
        alias="COD_ZDEM",
        title="ZDEM Code",
        description="The code for the ZDEM associated with this entry, used for identification purposes."
    )
    discount_type: str = Field(
        ...,
        alias="Tipo de descuento",
        title="Discount Type",
        description="Specifies the type of discount applied in this transaction, important for calculations."
    )
    recognition_type: str = Field(
        ...,
        alias="Tipo Reconocimiento",
        title="Recognition Type",
        description="Defines the recognition method for the transaction, indicating how it is categorized."
    )
    condition_application: str | float | None = Field(
        None,
        alias="Aplicación de condición",
        title="Condition Application",
        description="Details the application of specific conditions that affect this entry's processing."
    )
    type: str = Field(
        ...,
        alias="Tipo",
        title="Type",
        description="The classification type of this binnacle entry, aiding in its categorization."
    )
    value: float | str = Field(
        ...,
        alias="Valor",
        title="Value",
        description="The monetary value associated with this binnacle entry, critical for financial records."
    )
    consumption_condition: str | float | None = Field(
        None,
        alias="Condición consumo TM / % SoW",
        title="Consumption Condition",
        description="Describes the conditions under which consumption is measured in TM or Share of Wallet percentage."
    )
    stage: str = Field(
        ...,
        alias="ETAPA",
        title="Stage",
        description="Indicates the current stage of the process that this binnacle entry belongs to."
    )
    family: str = Field(
        ...,
        alias="FAMILIA",
        title="Family",
        description="Categorizes the product or entry into a specific family group for better organization."
    )
    product_code: PositiveInt | str = Field(
        ...,
        alias="COD_PRODUCTO",
        title="Product Code",
        description="A unique identifier for the product associated with this binnacle entry, essential for tracking."
    )

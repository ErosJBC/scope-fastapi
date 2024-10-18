"""
A module for client in the schemas package.
"""

from pydantic import BaseModel, Field, PositiveInt


class Client(BaseModel):
    """Client table representation for data validation from its Excel file"""

    cod_znje: PositiveInt = Field(
        ...,
        alias="COD_ZNJE",
        title="Client Type Code",
        description="A unique code that identifies the type of client in the system."
    )
    des_znje: str = Field(
        ...,
        alias="DES_ZNJE",
        title="Client Type Description",
        description="A detailed description of the client type to provide context."
    )
    cod_zent: PositiveInt = Field(
        ...,
        alias="COD_ZENT",
        title="Entity Code",
        description="The code representing the entity associated with the client."
    )
    cod_zdes: PositiveInt = Field(
        ...,
        alias="COD_ZDES",
        title="ZDES Code",
        description="The code that identifies the ZDES relevant to this client."
    )
    cod_zdem: PositiveInt = Field(
        ...,
        alias="COD_ZDEM",
        title="ZDEM Code",
        description="The code representing the ZDEM associated with this client."
    )
    des_country: str = Field(
        ...,
        alias="DES_PAIS",
        title="Country Description",
        description="The description of the country where the client is located."
    )

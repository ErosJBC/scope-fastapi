"""
A module for sale in the schemas package.
"""

from pydantic import BaseModel, Field, PositiveInt, PastDate


class Sale(BaseModel):
    """Sale table representation for data validation from its Excel file"""

    period: str | float = Field(
        ...,
        alias="Periodo",
        title="Period",
        description="The time frame for the sale, indicating the relevant month or year."
    )
    payment_responsible: PositiveInt = Field(
        ...,
        alias="Responsable de Pago",
        title="Payment Responsible",
        description="The identifier for the individual or entity responsible for making the payment."
    )
    payment_responsible_desc: str = Field(
        ...,
        alias="Desc Resp.Pago",
        title="Payment Responsible Description",
        description="A detailed description of the payment responsible party for better context."
    )
    current_territory: PositiveInt = Field(
        ...,
        alias="Territorio Actual",
        title="Current Territory",
        description="The identifier for the territory where the sale is taking place."
    )
    territory_desc: str = Field(
        ...,
        alias="Desc Territorio",
        title="Territory Description",
        description="A description of the current territory to provide additional context."
    )
    client: PositiveInt = Field(
        ...,
        alias="Cliente",
        title="Client",
        description="The identifier for the client involved in this sale."
    )
    client_desc: str = Field(
        ...,
        alias="Desc Cliente",
        title="Client Description",
        description="A detailed description of the client to provide context regarding their relationship."
    )
    variety_desc: str = Field(
        ...,
        alias="Desc Variedad",
        title="Variety Description",
        description="A description of the product variety being sold, providing additional classification."
    )
    family_desc: str = Field(
        ...,
        alias="Des Familia",
        title="Family Description",
        description="A description of the product family, helping to categorize the sale."
    )
    material: PositiveInt = Field(
        ...,
        alias="Material",
        title="Material",
        description="The identifier for the material associated with the sale."
    )
    material_desc: str = Field(
        ...,
        alias="Desc Material",
        title="Material Description",
        description="A description of the material involved in the sale, giving context to its classification."
    )
    invoice_class: str = Field(
        ...,
        alias="Clase de factura",
        title="Invoice Class",
        description="The classification of the invoice, providing insight into its type and use."
    )
    billing_doc: PositiveInt = Field(
        ...,
        alias="Doc.facturación",
        title="Billing Document",
        description="The identifier for the billing document associated with the sale."
    )
    reference: str = Field(
        ...,
        alias="Referencia",
        title="Reference",
        description="A reference code or identifier for tracking purposes related to the sale."
    )
    orders: PositiveInt = Field(
        ...,
        alias="Pedidos",
        title="Orders",
        description="The number of orders associated with this sale."
    )
    client_reference: str | float | None = Field(
        None,
        alias="Referencia clientes",
        title="Client Reference",
        description="A reference code used by the client for tracking this sale."
    )
    recipient_code: PositiveInt = Field(
        ...,
        alias="Codigo Destinatario",
        title="Recipient Code",
        description="The identifier for the recipient of the sale."
    )
    recipient: str = Field(
        ...,
        alias="Destinatario",
        title="Recipient",
        description="The name or designation of the recipient for this sale."
    )
    partners: str | float | None = Field(
        None,
        alias="Socios",
        title="Partners",
        description="Information about any partners involved in this sale, if applicable."
    )
    payment_condition: str = Field(
        ...,
        alias="Condicion de pago",
        title="Payment Condition",
        description="The terms of payment associated with this sale."
    )
    invoice_date: PastDate = Field(
        ...,
        alias="Fecha factura",
        title="Invoice Date",
        description="The date on which the invoice for the sale was issued, must be in the past."
    )
    billed_quantity: float = Field(
        ...,
        alias="Cantidad facturada",
        title="Billed Quantity",
        description="The total quantity billed in this sale."
    )
    tm: float = Field(
        ...,
        alias="TM",
        title="TM Value",
        description="The TM value associated with this sale, relevant for calculations."
    )
    net_value: float = Field(
        ...,
        alias="Valor neto",
        title="Net Value",
        description="The final net value of the sale after all adjustments and discounts."
    )
    p_base: float = Field(
        ...,
        alias="P_BASE",
        title="Base Price",
        description="The original base price before any discounts or modifications."
    )
    d_vol: float = Field(
        None,
        alias="D_VOL",
        title="Volume Discount",
        description="The discount applied based on the volume of products sold."
    )
    d_cot: float = Field(
        None,
        alias="D_COT",
        title="Cotización Discount",
        description="The discount applied based on the quotation provided."
    )
    d_cont: float = Field(
        None,
        alias="D_CONT",
        title="Contract Discount",
        description="The discount applied under the terms of a contract."
    )
    d_log: float = Field(
        None,
        alias="D_LOG",
        title="Logistics Discount",
        description="Any discounts provided related to logistics."
    )
    r_log: float = Field(
        None,
        alias="R_LOG",
        title="Logistics Rebate",
        description="Rebates related to logistics costs in the sale."
    )
    ncf: float = Field(
        ...,
        alias="NCF",
        title="NCF Code",
        description="The code associated with the NCF relevant to this sale."
    )
    p_neto: float = Field(
        ...,
        alias="P_NETO",
        title="Net Price",
        description="The final net price after applying all discounts and adjustments."
    )

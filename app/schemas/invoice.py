from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from ..schemas.baseSchema import MeasurementUnitEnum
from ..schemas import invoiceitem, customer


class InvoiceBase(BaseModel):
    amount: float
    date: Optional[date]
    profit: float
    customer_id: int

    class Config:
        orm_mode = True


class InvoiceCreate(InvoiceBase):
    invoice_items: list[invoiceitem.InvoiceItemBase]

    class Config:
        orm_mode = True


class Invoice(InvoiceBase):
    id: int

    class Config:
        orm_mode = True


class InvoiceWithInvoiceItems(Invoice):
    invoice_items: list[invoiceitem.InvoiceItem]

    class Config:
        orm_mode = True


class InvoiceWithCustomer(Invoice):
    customer: customer.CustomerBase

    class Config:
        orm_mode = True

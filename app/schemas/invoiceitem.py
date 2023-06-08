from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from ..schemas.baseSchema import MeasurementUnitEnum


class InvoiceItemBase(BaseModel):
    amount: float
    quantity: float
    unit_price: float
    product_id: float
    invoice_id: float

    class Config:
        orm_mode = True


class InvoiceItem(InvoiceItemBase):
    id: int

    class Config:
        orm_mode = True

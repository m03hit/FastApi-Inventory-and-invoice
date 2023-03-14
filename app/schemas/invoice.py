from datetime import date
from typing import List, Optional
from pydantic import BaseModel

class CustomerBase(BaseModel):
    id: int
    name: str
    mobile: int
    address: str
    class Config:
        orm_mode = True

class InvoiceBase(BaseModel):
    id: int
    amount: float
    date: date
    profit: float
    customer_id: int
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    id: int
    name: str
    total_quantity: float
    total_value: float
    measure_unit: str
    category_id: int
    class Config:
        orm_mode = True

class InvoiceItemWithProductDetails(BaseModel):
    id: int
    amount: float
    quantity: float
    unit_price: float
    product_id: float
    invoice_id: float
    product: ProductBase
    class Config:
        orm_mode = True

class Invoice(InvoiceBase):
    customer: CustomerBase
    invoice_items: list[InvoiceItemWithProductDetails]
    class Config:
        orm_mode = True
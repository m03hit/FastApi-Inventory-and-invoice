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


class ProductItemBase(BaseModel):
    id: int
    unit_price: float
    effective_unit_price: float
    total_value: float
    date_purchased: date
    quantity: float
    product_id: int

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
    product_item: ProductItemBase

    class Config:
        orm_mode = True


class Invoice(InvoiceBase):
    customer: CustomerBase
    invoice_items: list[InvoiceItemWithProductDetails]

    class Config:
        orm_mode = True


class InvoiceItemCreate(BaseModel):
    product_id: float
    quantity: float
    unit_price: float
    amount: float
    product_item_id: float

    class Config:
        orm_mode = True


class InvoiceItemCreated(BaseModel):
    id: int
    amount: float
    quantity: float
    unit_price: float
    product_id: float
    product: ProductBase
    product_item: ProductItemBase

    class Config:
        orm_mode = True


class InvoiceCreate(BaseModel):
    customer_id: int
    date: date
    amount: float
    profit: float
    invoice_items: list[InvoiceItemCreate]

    class Config:
        orm_mode = True


class InvoiceCreated(BaseModel):
    id: int
    amount: float
    date: date
    profit: float
    customer: CustomerBase
    invoice_items: list[InvoiceItemCreated]

    class Config:
        orm_mode = True

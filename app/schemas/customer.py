from datetime import date
from typing import List, Optional
from pydantic import BaseModel

class InvoiceBase(BaseModel):
    id: int
    amount: float
    date: date
    profit: float
    customer_id: int
    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    id: int
    name: str
    mobile: int
    address: str
    class Config:
        orm_mode = True

class Customer(CustomerBase):
    invoices: list[InvoiceBase] = []
    class Config:
        orm_mode = True


class CreateCustomer(BaseModel):
    name: str
    mobile: int
    address: str
    class Config:
        orm_mode = True
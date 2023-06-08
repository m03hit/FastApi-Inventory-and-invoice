from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class CustomerBase(BaseModel):
    name: str
    mobile: int
    address: str

    class Config:
        orm_mode = True


class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True


from ..schemas import invoice


class CustomerWithInvoices(Customer):
    invoices: list[invoice.Invoice] = []

    class Config:
        orm_mode = True

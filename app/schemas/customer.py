from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from . import customer,invoice,invoiceitem,product,productcategory,productimage,productitem,purchase,purchaseexpense,purchaseitem,supplier




class CustomerBase(BaseModel):
    id: int
    name: str
    mobile: int
    address: str
    class Config:
        orm_mode = True

class Customer(CustomerBase):
    invoices: list[invoice.InvoiceBase] = []
    class Config:
        orm_mode = True


class CreateCustomer(BaseModel):
    name: str
    mobile: int
    address: str
    class Config:
        orm_mode = True
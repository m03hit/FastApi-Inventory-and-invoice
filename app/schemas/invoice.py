from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from . import customer,invoice,invoiceitem,product,productcategory,productimage,productitem,purchase,purchaseexpense,purchaseitem,supplier

class InvoiceBase(BaseModel):
    id: int
    amount: float
    date: date
    profit: float
    customer_id: int
    class Config:
        orm_mode = True

class Invoice(InvoiceBase):
    invoice_items: list[invoiceitem.InvoiceItemWithProductDetails]
    customer: customer.CustomerBase
    class Config:
        orm_mode = True
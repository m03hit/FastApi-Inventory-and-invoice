from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from . import customer,invoice,invoiceitem,product,productcategory,productimage,productitem,purchase,purchaseexpense,purchaseitem,supplier

class SupplierBase(BaseModel):
    id: int
    name: str
    mobile: int
    class Config:
        orm_mode = True

class Supplier(SupplierBase):
    supplier_purchases: list[purchase.PurchaseBase] = []
    class Config:
        orm_mode = True
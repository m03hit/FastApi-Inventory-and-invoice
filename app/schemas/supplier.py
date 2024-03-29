from datetime import date
from typing import List, Optional
from pydantic import BaseModel

######## move it
# class PurchaseBase(BaseModel):
#     id: int
#     date: Optional[date]
#     title: str
#     amount: float
#     supplier_id: float

#     class Config:
#         orm_mode = True


class SupplierBase(BaseModel):
    name: str
    mobile: int

    class Config:
        orm_mode = True


class Supplier(SupplierBase):
    id: int

    class Config:
        orm_mode = True


from ..schemas import purchase


class SupplierWithPurchases(Supplier):
    supplier_purchases: list[purchase.Purchase] = []

    class Config:
        orm_mode = True

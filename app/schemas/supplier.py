from datetime import date
from typing import List, Optional
from pydantic import BaseModel

class PurchaseBase(BaseModel):
    id: int
    date: date
    title: str
    amount: float
    supplier_id: float
    class Config:
        orm_mode = True

class SupplierBase(BaseModel):
    id: int
    name: str
    mobile: int
    class Config:
        orm_mode = True

class Supplier(SupplierBase):
    supplier_purchases: list[PurchaseBase] = []
    class Config:
        orm_mode = True
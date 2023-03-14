from datetime import date
from typing import List, Optional
from pydantic import BaseModel

class SupplierBase(BaseModel):
    id: int
    name: str
    mobile: int
    class Config:
        orm_mode = True

class PurchaseItemBase(BaseModel):
    id: int
    quantity: float
    unit_price: float
    amount: float
    product_id: int
    purchase_id: int
    class Config:
        orm_mode = True

class PurchaseExpenseBase(BaseModel):
    id: int
    amount: float
    title: str
    description: str
    purchase_id: str
    class Config:
        orm_mode = True

class PurchaseBase(BaseModel):
    id: int
    date: date
    title: str
    amount: float
    supplier_id: float
    class Config:
        orm_mode = True

class Purchase(PurchaseBase):
    supplier: SupplierBase
    purchase_items: list[PurchaseItemBase] = []
    purchase_expenses: list[PurchaseExpenseBase] = []
    class Config:
        orm_mode = True
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


class PurchaseExpenseBase(BaseModel):
    id: int
    amount: float
    title: str
    description: str
    purchase_id: str

    class Config:
        orm_mode = True


class PurchaseExpense(PurchaseExpenseBase):
    purchase: PurchaseBase

    class Config:
        orm_mode = True

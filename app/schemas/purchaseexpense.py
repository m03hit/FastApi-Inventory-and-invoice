from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class PurchaseBase(BaseModel):
    date: Optional[date]
    title: str
    amount: float
    supplier_id: int

    class Config:
        orm_mode = True


class PurchaseExpenseBase(BaseModel):
    amount: float
    title: str
    description: str

    class Config:
        orm_mode = True


class PurchaseExpense(PurchaseExpenseBase):
    id: int

    class Config:
        orm_mode = True


class PurchaseExpenseWithPurchase(PurchaseExpense):
    id: int
    purchase: PurchaseBase

    class Config:
        orm_mode = True

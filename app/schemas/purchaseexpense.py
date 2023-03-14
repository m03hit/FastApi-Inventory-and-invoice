from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from . import customer,invoice,invoiceitem,product,productcategory,productimage,productitem,purchase,purchaseexpense,purchaseitem,supplier


class PurchaseExpenseBase(BaseModel):
    id: int
    amount: float
    title: str
    description: str
    purchase_id: str
    class Config:
        orm_mode = True

class PurchaseExpense(PurchaseExpenseBase):
    purchase: purchase.PurchaseBase
    class Config:
        orm_mode = True

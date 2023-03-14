from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from . import customer,invoice,invoiceitem,product,productcategory,productimage,productitem,purchase,purchaseexpense,purchaseitem,supplier

class PurchaseBase(BaseModel):
    id: int
    date: date
    title: str
    amount: float
    supplier_id: float
    class Config:
        orm_mode = True

class Purchase(PurchaseBase):
    supplier: supplier.SupplierBase
    purchase_items: list[purchaseitem.PurchaseItemBase] = []
    purchase_expenses: list[purchaseexpense.PurchaseExpenseBase] = []
    class Config:
        orm_mode = True
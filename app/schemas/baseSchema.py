from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from ..schemas import supplier
from ..schemas import productitem, purchaseexpense


class PurchaseBase(BaseModel):
    date: Optional[date]
    title: str
    amount: float
    supplier_id: float

    class Config:
        orm_mode = True


class Purchase(PurchaseBase):
    id: int

    class Config:
        orm_mode = True


class PurchaseWithProductsAndExpenses(Purchase):
    supplier: supplier.Supplier
    products: list[productitem.ProductItem] = []
    purchase_expenses: list[purchaseexpense.PurchaseExpense] = []

    class Config:
        orm_mode = True


class PurchaseCreate(PurchaseBase):
    products: list[productitem.ProductItemBase]
    purchase_expenses: list[purchaseexpense.PurchaseExpenseBase]

    class Config:
        orm_mode = True

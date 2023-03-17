from datetime import date
from typing import List, Optional
from pydantic import BaseModel

class SupplierBase(BaseModel):
    id: int
    name: str
    mobile: int
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

class ProductItemBase(BaseModel):
    id: int
    unit_price: float
    effective_unit_price: float
    total_value: float
    date_purchased: date
    quantity: float
    product_id: int
    class Config:
        orm_mode = True

class Purchase(PurchaseBase):
    supplier: SupplierBase
    products: list[ProductItemBase] = []
    purchase_expenses: list[PurchaseExpenseBase] = []
    class Config:
        orm_mode = True

class ProductItemCreate(BaseModel):
    unit_price: float
    effective_unit_price: float
    date_purchased: date
    quantity: float
    product_id: int
    class Config:
        orm_mode = True

class PurchaseExpenseCreate(BaseModel):
    amount: float
    title: str
    description: str
    class Config:
        orm_mode = True

class PurchaseCreate(BaseModel):
    date: date
    title: str
    amount: float
    supplier_id: int
    products: list[ProductItemCreate]
    purchase_expenses: list[PurchaseExpenseCreate]

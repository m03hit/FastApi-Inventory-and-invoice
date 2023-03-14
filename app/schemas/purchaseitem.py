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

class ProductBase(BaseModel):
    id: int
    name: str
    total_quantity: float
    total_value: float
    measure_unit: str
    category_id: int
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

class PurchaseItems(PurchaseItemBase):
    purchase: PurchaseBase
    product: ProductBase
    class Config:
        orm_mode = True
from datetime import date
from typing import List, Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    id: int
    name: str
    total_quantity: float
    total_value: float
    measure_unit: str
    category_id: int
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

class ProductItem(ProductItemBase):
    product: ProductBase
    class Config:
        orm_mode = True
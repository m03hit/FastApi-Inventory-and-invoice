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

class ProductCategoryBase(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class ProductCategory(ProductCategoryBase):
    products: list[ProductBase] = []
    class Config:
        orm_mode = True
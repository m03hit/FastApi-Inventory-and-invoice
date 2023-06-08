from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel
from ..schemas.product import MeasurementUnitEnum
from ..schemas import product


class ProductCategoryBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ProductCategory(ProductCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProductCategoryWithProducts(ProductCategory):
    products: list[product.ProductBase] = []

    class Config:
        orm_mode = True

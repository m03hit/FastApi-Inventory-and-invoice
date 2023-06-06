from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel
from ..schemas.product import MeasurementUnitEnum


class ProductBase(BaseModel):
    id: int
    name: str
    total_quantity: float
    total_value: float
    measurement_unit: MeasurementUnitEnum
    category_id: int

    class Config:
        orm_mode = True


class ProductCategoryBase(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProductCategory(ProductCategoryBase):
    products: list[ProductBase] = []

    class Config:
        orm_mode = True


class ProductCategoryCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True

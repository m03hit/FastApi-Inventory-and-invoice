from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from ..schemas.product import MeasurementUnitEnum


# date auto or manual , should even be included ?


class ProductBase(BaseModel):
    id: int
    name: str
    total_quantity: float
    total_value: float
    measurement_unit: MeasurementUnitEnum
    category_id: int

    class Config:
        orm_mode = True


class ProductItemBase(BaseModel):
    unit_price: float
    effective_unit_price: float
    total_value: float
    quantity: float
    product_id: int

    class Config:
        orm_mode = True


class ProductItem(ProductItemBase):
    id: int
    date_purchased: Optional[date]

    class Config:
        orm_mode = True


class ProductItemWithProduct(ProductItem):
    product: ProductBase

    class Config:
        orm_mode = True

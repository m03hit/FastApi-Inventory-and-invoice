from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from ..schemas import product

# date auto or manual , should even be included ?


class ProductItemBase(BaseModel):
    date_purchased: Optional[date]
    unit_price: float
    effective_unit_price: float
    total_value: float
    quantity: float
    product_id: int

    class Config:
        orm_mode = True


class ProductItem(ProductItemBase):
    id: int

    class Config:
        orm_mode = True

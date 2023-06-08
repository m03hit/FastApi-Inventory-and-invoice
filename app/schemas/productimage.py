from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class ProductImageBase(BaseModel):
    image_url: str
    product_id: int

    class Config:
        orm_mode = True


class ProductImage(ProductImageBase):
    id: int

    class Config:
        orm_mode = True


from ..schemas.product import ProductBase


class ProductImageWithProduct(ProductImage):
    product: ProductBase

    class Config:
        orm_mode = True

from datetime import date
from typing import List, Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    id: int
    name: str
    #total_quantity: float
    #total_value: float
    measure_unit: str
    category_id: int
    class Config:
        orm_mode = True

class ProductImageBase(BaseModel):
    id: int
    image_url: str
    product_id: int
    class Config:
        orm_mode = True

class ProductImage(ProductImageBase):
    product: ProductBase
    class Config:
        orm_mode = True

class ProductImageCreate(BaseModel):
    image_url: str
    product_id: int
    class Config:
        orm_mode = True

class ProductImageCreated(BaseModel):
    id: int
    image_url: str
    product: ProductBase
    class Config:
        orm_mode = True    
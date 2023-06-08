from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel
from ..schemas.baseSchema import MeasurementUnitEnum


class ProductBase(BaseModel):
    name: str
    measurement_way_id: int
    measurement_unit: MeasurementUnitEnum
    category_id: int

    class Config:
        orm_mode = True


class Product(ProductBase):
    id: int
    total_quantity: float
    total_value: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


from ..schemas import productimage, productitem


class ProductCreate(ProductBase):
    product_images: list[str]

    class Config:
        orm_mode = True


class ProductWithProductImages(Product):
    product_images: list[productimage.ProductImage]

    class Config:
        orm_mode = True


class ProductWithProductItems(ProductWithProductImages):
    product_items: list[productitem.ProductItem] = []

    class Config:
        orm_mode = True


# def dict(self, *args, **kwargs):
#     product_dict = super().dict(*args, **kwargs)
#     category_dict = self.product_category.__dict__
#     category_dict["product_category_id"] = category_dict.pop("id")
#     category_dict.pop("name")
#     product_dict.update(category_dict)
#     product_dict.pop("product_category")
#     return product_dict

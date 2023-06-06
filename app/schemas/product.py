from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class MeasurementUnitEnum(str, Enum):
    sqfeet = "sqfeet"
    piece = "piece"


class ProductCategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class InvoiceItemBase(BaseModel):
    id: int
    amount: float
    quantity: float
    unit_price: float
    product_id: float
    invoice_id: float

    class Config:
        orm_mode = True


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
    measurement_unit: MeasurementUnitEnum
    category_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProductImageBase(BaseModel):
    image_url: str

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


class ProductWithoutProductItems(ProductBase):
    product_category: ProductCategoryBase
    product_images: list[ProductImageBase] = []

    def dict(self, *args, **kwargs):
        product_dict = super().dict(*args, **kwargs)
        category_dict = self.product_category.__dict__
        category_dict["product_category_id"] = category_dict.pop("id")
        category_dict.pop("name")
        product_dict.update(category_dict)
        product_dict.pop("product_category")
        return product_dict

    class Config:
        orm_mode = True


class ProductWithProductItems(ProductWithoutProductItems):
    product_items: list[ProductItemBase] = []

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    name: str
    measurement_unit: MeasurementUnitEnum
    category_id: int
    product_images: list[str]

    class Config:
        orm_mode = True


class ProductCreated(ProductCreate):
    id: int
    product_images: list[ProductImageBase]

    class Config:
        orm_mode = True

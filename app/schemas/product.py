from datetime import date
from typing import List, Optional
from pydantic import BaseModel

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

class Product(ProductBase):
    product_category: ProductCategoryBase
    product_items: list[ProductItemBase] = []
    product_images: list[ProductImageBase] = []
    product_purchases: list[PurchaseBase] = []
    invoice_items: list[InvoiceItemBase] = []
    class Config:
        orm_mode = True
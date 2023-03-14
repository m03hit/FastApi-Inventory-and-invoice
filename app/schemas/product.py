from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from . import customer,invoice,invoiceitem,product,productcategory,productimage,productitem,purchase,purchaseexpense,purchaseitem,supplier

class ProductBase(BaseModel):
    id: int
    name: str
    total_quantity: float
    total_value: float
    measure_unit: str
    category_id: int
    class Config:
        orm_mode = True



class Product(ProductBase):
    product_category: productcategory.ProductCategoryBase
    product_items: list[productitem.ProductItemBase] = []
    product_images: list[productimage.ProductImageBase] = []
    product_purchases: list[purchase.PurchaseBase] = []
    invoice_items: list[invoiceitem.InvoiceItemBase] = []
    class Config:
        orm_mode = True
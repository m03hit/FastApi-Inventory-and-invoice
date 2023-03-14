from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from . import customer,invoice,invoiceitem,product,productcategory,productimage,productitem,purchase,purchaseexpense,purchaseitem,supplier





class ProductImageBase(BaseModel):
    id: int
    image_url: str
    product_id: int
    class Config:
        orm_mode = True

class ProductImage(ProductImageBase):
    product: product.ProductBase
    class Config:
        orm_mode = True
from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from . import customer,invoice,invoiceitem,product,productcategory,productimage,productitem,purchase,purchaseexpense,purchaseitem,supplier



class ProductCategoryBase(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class ProductCategory(ProductCategoryBase):
    products: list[product.ProductBase] = []
    class Config:
        orm_mode = True
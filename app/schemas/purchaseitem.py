from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from . import customer,invoice,invoiceitem,product,productcategory,productimage,productitem,purchase,purchaseexpense,purchaseitem,supplier




class PurchaseItemBase(BaseModel):
    id: int
    quantity: float
    unit_price: float
    amount: float
    product_id: int
    purchase_id: int
    class Config:
        orm_mode = True

class PurchaseItems(PurchaseItemBase):
    purchase: purchase.PurchaseBase
    product: product.ProductBase
    class Config:
        orm_mode = True
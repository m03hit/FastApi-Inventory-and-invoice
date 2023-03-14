from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from . import customer,invoice,invoiceitem,product,productcategory,productimage,productitem,purchase,purchaseexpense,purchaseitem,supplier

class InvoiceItemBase(BaseModel):
    id: int
    amount: float
    quantity: float
    unit_price: float
    product_id: float
    invoice_id: float
    class Config:
        orm_mode = True

class InvoiceItemWithProductDetails(InvoiceItemBase):
    product: product.ProductBase
    class Config:
        orm_mode = True



class InvoiceItem(InvoiceItemBase):
    product: product.ProductBase
    invoice: invoice.InvoiceBase
    class Config:
        orm_mode = True
from datetime import date
from typing import List, Optional
from pydantic import BaseModel

class CustomerBase(BaseModel):
    id: int
    name: str
    mobile: int
    address: str
    class Config:
        orm_mode = True

class ProductCategoryBase(BaseModel):
    id: int
    name: str
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

class InvoiceBase(BaseModel):
    id: int
    amount: float
    date: date
    profit: float
    customer_id: int
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

class SupplierBase(BaseModel):
    id: int
    name: str
    mobile: int
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

class PurchaseItemBase(BaseModel):
    id: int
    quantity: float
    unit_price: float
    amount: float
    product_id: int
    purchase_id: int
    class Config:
        orm_mode = True

class PurchaseExpenseBase(BaseModel):
    id: int
    amount: float
    title: str
    description: str
    purchase_id: str
    class Config:
        orm_mode = True

class Customer(CustomerBase):
    invoices: list[InvoiceBase] = []
    class Config:
        orm_mode = True

class ProductCategory(ProductCategoryBase):
    products: list[ProductBase] = []
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

class ProductItem(ProductItemBase):
    product: ProductBase
    class Config:
        orm_mode = True

class ProductImage(ProductImageBase):
    product: ProductBase
    class Config:
        orm_mode = True

class Supplier(SupplierBase):
    supplier_purchases: list[PurchaseBase] = []
    class Config:
        orm_mode = True

class Purchase(PurchaseBase):
    supplier: SupplierBase
    purchase_items: list[PurchaseItemBase] = []
    purchase_expenses: list[PurchaseExpenseBase] = []
    class Config:
        orm_mode = True

class PurchaseItems(PurchaseItemBase):
    purchase: PurchaseBase
    product: ProductBase
    class Config:
        orm_mode = True

class PurchaseExpense(PurchaseExpenseBase):
    purchase: PurchaseBase
    class Config:
        orm_mode = True

class Invoice(InvoiceBase):
    invoice_items: list[InvoiceItemBase]
    customer: CustomerBase
    class Config:
        orm_mode = True

class InvoiceItem(InvoiceItemBase):
    product: ProductBase
    invoice: InvoiceBase
    class Config:
        orm_mode = True
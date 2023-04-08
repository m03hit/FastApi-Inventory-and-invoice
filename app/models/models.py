from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Date,
    BigInteger,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..database.database import Base


class ProductCategory(Base):
    __tablename__ = "product_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )
    products = relationship("Product", back_populates="product_category")


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mobile = Column(BigInteger)
    address = Column(String)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False)
    invoices = relationship("Invoice", back_populates="customer")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    total_quantity = Column(Float, default=0)
    total_value = Column(Float, default=0)
    measure_unit = Column(String)
    selling_unit = Column(String)
    category_id = Column(Integer, ForeignKey("product_categories.id"))
    product_category = relationship("ProductCategory", back_populates="products")
    product_items = relationship("ProductItem", back_populates="product")
    product_images = relationship("ProductImage", back_populates="product")
    invoice_items = relationship("InvoiceItem", back_populates="product")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )


class ProductItem(Base):
    __tablename__ = "product_items"
    id = Column(Integer, primary_key=True, index=True)
    unit_price = Column(Float)
    effective_unit_price = Column(Float)
    total_value = Column(Float)
    date_purchased = Column(Date)
    quantity = Column(Float)
    purchase_id = Column(Integer, ForeignKey("purchases.id"))
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="product_items")
    purchase = relationship("Purchase", back_populates="products")


class ProductImage(Base):
    __tablename__ = "product_images"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="product_images")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mobile = Column(BigInteger)
    supplier_purchases = relationship("Purchase", back_populates="supplier")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )


class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    title = Column(String)
    amount = Column(String, default=0)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    supplier = relationship("Supplier", back_populates="supplier_purchases")
    purchase_expenses = relationship("PurchaseExpense", back_populates="purchase")
    products = relationship("ProductItem", back_populates="purchase")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )


class PurchaseExpense(Base):
    __tablename__ = "purchase_expenses"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    title = Column(String)
    description = Column(String)
    purchase_id = Column(Integer, ForeignKey("purchases.id"))
    purchase = relationship("Purchase", back_populates="purchase_expenses")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    date = Column(Date)
    profit = Column(Float)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="invoices")
    invoice_items = relationship("InvoiceItem", back_populates="invoice")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    quantity = Column(Float)
    unit_price = Column(Float)
    product_id = Column(Integer, ForeignKey("products.id"))
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    product = relationship("Product", back_populates="invoice_items")
    invoice = relationship("Invoice", back_populates="invoice_items")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )

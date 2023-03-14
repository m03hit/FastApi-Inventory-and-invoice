from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from ..database import Base


class ProductCategory(Base):
	__tablename__ = "product_categories"
	id = Column(Integer,primary_key=True,index=True)
	name = Column(String)
	products = relationship("Product",back_populates="product_category")

class Customer(Base):
	__tablename__ = "customers"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	mobile = Column(Integer)    
	address = Column(String)
	invoices = relationship("Invoice",back_populates="customer")

class Product(Base):
	__tablename__ = "products"
	id = Column(Integer,primary_key=True,index=True)
	name = Column(String)
	total_quantity = Column(Float)	
	total_value = Column(Float)
	measure_unit = Column(String)
	category_id = Column(Integer,ForeignKey("product_categories.id"))
	product_category = relationship("ProductCategory", back_populates="products")
	product_items = relationship("ProductItem",back_populates="product")
	product_images = relationship("ProductImage",back_populates="product")
	product_purchases = relationship("PurchaseItem",back_populates="product")
	invoice_items = relationship("InvoiceItem",back_populates="product")
	

class ProductItem(Base):
	__tablename__ = "product_items"
	id = Column(Integer,primary_key=True,index=True)
	unit_price = Column(Float)
	effective_unit_price = Column(Float)
	total_value = Column(Float)
	date_purchased = Column(Date)
	quantity = Column(Float)
	product_id = Column(Integer,ForeignKey("products.id"))
	product = relationship("Product",back_populates="product_items")

class ProductImage(Base):
	__tablename__ = "product_images"
	id = Column(Integer,primary_key=True,index=True)
	image_url = Column(String)
	product_id = Column(Integer,ForeignKey("products.id"))
	product = relationship("Product",back_populates="product_images")


class Supplier(Base):
	__tablename__ = "suppliers"
	id = Column(Integer,primary_key=True,index=True)
	name = Column(String)
	mobile = Column(Integer)
	supplier_purchases = relationship("Purchase",back_populates="supplier")

class Purchase(Base):
	__tablename__ = "purchases"
	id = Column(Integer,primary_key=True,index=True)
	date = Column(Date)
	title = Column(String)
	amount = Column(String)
	supplier_id = Column(Integer,ForeignKey("suppliers.id"))
	supplier = relationship("Supplier",back_populates="supplier_purchases")
	purchase_items = relationship("PurchaseItem",back_populates="purchase")
	purchase_expenses = relationship("PurchaseExpense",back_populates="purchase")


class PurchaseItem(Base):
	__tablename__ = "purchase_items"
	id = Column(Integer,primary_key=True,index=True)
	quantity = Column(Float)
	unit_price = Column(Float)
	amount = Column(Float)
	product_id = Column(Integer,ForeignKey("products.id"))
	purchase_id = Column(Integer,ForeignKey("purchases.id"))
	purchase = relationship("Purchase",back_populates="purchase_items")
	product = relationship("Product",back_populates="product_purchases")

class PurchaseExpense(Base):
	__tablename__ = "purchase_expenses"
	id = Column(Integer,primary_key=True,index=True)
	amount = Column(Float)
	title = Column(String)
	description = Column(Float)
	purchase_id = Column(Integer,ForeignKey("purchases.id"))
	purchase = relationship("Purchase",back_populates="purchase_expenses")

class Invoice(Base):
	__tablename__ = "invoices"
	id = Column(Integer,primary_key=True,index=True)
	amount = Column(Float)	
	date = Column(Date)
	profit = Column(Float)
	customer_id = Column(Integer,ForeignKey("customers.id"))
	customer = relationship("Customer",back_populates="invoices")
	invoice_items = relationship("InvoiceItem",back_populates="invoice")

class InvoiceItem(Base):
	__tablename__ = "invoice_items"
	id = Column(Integer,primary_key=True,index=True)
	amount = Column(Float)	
	quantity = Column(Float)	
	unit_price = Column(Float)	
	product_id = Column(Integer,ForeignKey("products.id"))
	invoice_id = Column(Integer,ForeignKey("invoices.id"))
	product = relationship("Product",back_populates="invoice_items")
	invoice = relationship("Invoice",back_populates="invoice_items")


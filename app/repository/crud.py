from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models import models
from ..schemas import (
    customer,
    invoice,
    productcategory,
    supplier,
    productimage,
    product,
    purchase,
)


##### CUSTOMERS #######


def get_customers(db: Session):
    return db.query(models.Customer).all()


def get_customer(db: Session, id: int):
    return db.query(models.Customer).filter(models.Customer.id == id).first()


def create_customer(db: Session, user: customer.CustomerBase):
    db_customer = models.Customer(
        name=user.name, mobile=user.mobile, address=user.address
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customer_by_mobile(db: Session, mobile: int):
    return db.query(models.Customer).filter(models.Customer.mobile == mobile).first()


def delete_customer(db: Session, id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == id)

    if not customer.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no customer exists with id - {id} ",
        )

    customer.delete(synchronize_session=False)
    db.commit()
    return "done"


# Category


def does_category_exists(db: Session, id: int):
    category = (
        db.query(models.ProductCategory).filter(models.ProductCategory.id == id).first()
    )
    if not category:
        return False
    return True


def create_category(db: Session, category: productcategory.ProductCategoryBase):
    p_category = models.ProductCategory(name=category.name)
    db.add(p_category)
    db.commit()
    db.refresh(p_category)
    return p_category


def get_product_categories(db: Session):
    return db.query(models.ProductCategory).all()


def get_product_category(id: int, db: Session):
    product_category = (
        db.query(models.ProductCategory).filter(models.ProductCategory.id == id).first()
    )
    if not product_category:
        return -1
    return product_category


def does_measurement_way_exists(db: Session, id: int):
    measurement_way = (
        db.query(models.MeasurementWay).filter(models.MeasurementWay.id == id).first()
    )
    if not measurement_way:
        return False
    return True


# Invoice #######


def get_invoice(db: Session, id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == id).first()


def get_invoices(db: Session):
    return db.query(models.Invoice).all()


def create_invoice(db: Session, invoice: invoice.InvoiceBase):
    db_invoice = models.Invoice(
        amount=invoice.amount,
        date=invoice.date,
        profit=0,
        customer_id=invoice.customer_id,
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def create_invoice_items(
    db: Session, invoice: invoice.InvoiceBase, invoice_id_int: int
):
    print(invoice.invoice_items)
    for item in invoice.invoice_items:
        db.add(
            models.InvoiceItem(
                amount=item.amount,
                unit_price=item.unit_price,
                quantity=item.quantity,
                product_id=item.product_id,
                invoice_id=invoice_id_int,
                product_item_id=1,
            )
        )

    # db.add_all(invoice.invoice_items)
    db.commit()


## Supplier


def create_supplier(supplier: supplier.SupplierBase, db: Session):
    create_supplier = models.Supplier(name=supplier.name, mobile=supplier.mobile)
    db.add(create_supplier)
    db.commit()
    db.refresh(create_supplier)
    return create_supplier


def get_suppliers(db: Session):
    return db.query(models.Supplier).all()


def get_supplier(id: int, db: Session):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == id).first()
    return supplier


def get_supplier_by_mobile_no(mobile: int, db: Session):
    return db.query(models.Supplier).filter(models.Supplier.mobile == mobile).first()


## Products


def create_product(product: product.ProductCreate, db: Session):
    product_to_add = models.Product(
        name=product.name,
        measurement_unit=product.measurement_unit,
        category_id=product.category_id,
        measurement_way_id=product.measurement_way_id,
    )
    db.add(product_to_add)
    db.commit()
    db.refresh(product_to_add)
    return product_to_add


def get_products(db: Session):
    return db.query(models.Product).all()


def read_product(id: int, db: Session):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    return product


# Purchases


def read_purchase(id: int, db: Session):
    return db.query(models.Purchase).filter(models.Purchase.id == id).first()


def read_purchases(db: Session):
    return db.query(models.Purchase).all()


# def create_purchase(purchase:purchase.PurchaseCreate,db:Session):


## images


def create_image(p_id: int, db: Session, img_url: str):
    image = models.ProductImage(image_url=img_url, product_id=p_id)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def read_image(id: int, db: Session):
    return db.query(models.ProductImage).filter(models.ProductImage.id == id).first()


def read_images(db: Session):
    return db.query(models.ProductImage).all()

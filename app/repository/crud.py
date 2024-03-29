from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import update
from ..models import models
from ..schemas import (
    customer,
    invoice,
    productcategory,
    supplier,
    productimage,
    product,
    purchase,
    purchaseexpense,
    productitem,
    invoiceitem,
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


def create_invoice_items(db: Session, invoice_items: list[invoiceitem.InvoiceItemBase]):
    for i_item in invoice_items:
        db.add(i_item)
        print(i_item.__dict__)
        current_stock = (
            db.query(models.ProductItem.quantity)
            .filter(models.ProductItem.id == i_item.product_item_id)
            .scalar()
        )
        stmt = (
            update(models.ProductItem)
            .where(models.ProductItem.id == i_item.product_item_id)
            .values(quantity=current_stock - i_item.quantity)
        )
        db.execute(stmt)
    db.commit()
    # db.add_all(invoice_items)
    # db.commit()
    # for item in invoice.invoice_items:
    #     db.add(
    #         models.InvoiceItem(
    #             amount=item.amount,
    #             unit_price=item.unit_price,
    #             quantity=item.quantity,
    #             product_id=item.product_id,
    #             invoice_id=invoice_id_int,
    #             product_item_id=1,
    #         )
    #     )

    # db.add_all(invoice.invoice_items)


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


def create_purchase(purchase: purchase.PurchaseCreate, db: Session):
    purchase_to_add = models.Purchase(
        date=purchase.date,
        title=purchase.title,
        amount=purchase.amount,
        supplier_id=purchase.supplier_id,
    )
    db.add(purchase_to_add)
    db.commit()
    db.refresh(purchase_to_add)
    return purchase_to_add


# Purchase Expenses


def create_purchase_expenses(
    purchase_id: int, expenses: list[purchaseexpense.PurchaseExpenseBase], db: Session
):
    expenses_list_model = []
    for expense in expenses:
        expenses_list_model.append(
            models.PurchaseExpense(
                purchase_id=purchase_id,
                amount=expense.amount,
                title=expense.title,
                description=expense.description,
            )
        )
    db.add_all(expenses_list_model)
    db.commit()


def read_purchase_expense(id: int, db: Session):
    return (
        db.query(models.PurchaseExpense).filter(models.PurchaseExpense.id == id).first()
    )


def read_purchase_expenses(db: Session):
    return db.query(models.PurchaseExpense).all()


## Product Items


def create_product_items(
    product_items: list[productitem.ProductItemBase], purchase_id: int, db: Session
):
    product_item_list_model = []
    for p_item in product_items:
        product_item_list_model.append(
            models.ProductItem(
                unit_price=p_item.unit_price,
                effective_unit_price=p_item.effective_unit_price,
                total_value=p_item.effective_unit_price * p_item.quantity,
                date_purchased=p_item.date_purchased,
                quantity=p_item.quantity,
                purchase_id=purchase_id,
                product_id=p_item.product_id,
            )
        )
    db.add_all(product_item_list_model)
    db.commit()


def update_total_quantity(product_ids: list[int], db: Session):
    for pid in product_ids:
        total_product_quantity = (
            db.query(func.sum(models.ProductItem.quantity))
            .filter(models.ProductItem.product_id == pid)
            .scalar()
        )
        total_product_quantity = total_product_quantity or 0
        print(f"productid {pid}", total_product_quantity)
        stmt = (
            update(models.Product)
            .where(models.Product.id == pid)
            .values(total_quantity=total_product_quantity)
        )
        db.execute(stmt)
        db.commit()
        # stmt = (
        #     update(models.Product)
        #     .where(models.Product.id == pid)
        #     .values(total_quantity=total_product_quantity)
        # )
        # db.query(models.Product).filter(models.Product.id == id).update(
        #    {"total_quantity": total_product_quantity}
        # )
        # db.commit()


# def create_purchase(purchase:purchase.PurchaseCreate,db:Session):


def update_total_value_in_product_and_items(db: Session):
    updateitemvalue = update(models.ProductItem).values(
        total_value=models.ProductItem.quantity
        * models.ProductItem.effective_unit_price
    )
    db.execute(updateitemvalue)
    db.commit()

    all_products = db.query(models.Product).all()

    for product in all_products:
        product_value = (
            db.query(func.sum(models.ProductItem.total_value))
            .filter(models.ProductItem.product_id == product.id)
            .scalar()
        )
        product_value = product_value or 0
        stmt = (
            update(models.Product)
            .where(models.Product.id == product.id)
            .values(total_value=product_value)
        )
        db.execute(stmt)
    db.commit()


## images


def create_images(p_id: int, db: Session, img_urls: list[str]):
    product_image_model_list = []
    for i_url in img_urls:
        image = models.ProductImage(image_url=i_url, product_id=p_id)
        product_image_model_list.append(image)

    db.add_all(product_image_model_list)
    a = db.commit()


def read_image(id: int, db: Session):
    return db.query(models.ProductImage).filter(models.ProductImage.id == id).first()


def read_images(db: Session):
    return db.query(models.ProductImage).all()


def get_total_quantity_of_product(product_id: int, db: Session):
    return (
        db.query(models.Product.total_quantity)
        .filter(models.Product.id == product_id)
        .scalar()
    )


# ProductItems


def read_product_items_by_p_id(product_id: int, db: Session):
    return (
        db.query(models.ProductItem)
        .filter(models.ProductItem.product_id == product_id)
        .order_by(models.ProductItem.id)
        .all()
    )

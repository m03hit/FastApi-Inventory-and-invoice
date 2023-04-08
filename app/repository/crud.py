from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models import models
from ..schemas import customer, invoice


##### CUSTOMERS #######


def get_customers(db: Session):
    return db.query(models.Customer).all()


def get_customer(db: Session, id: int):
    return db.query(models.Customer).filter(models.Customer.id == id).first()


def create_customer(db: Session, user: customer.CreateCustomer):
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


# Invoice #######


def get_invoice(db: Session, id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == id).first()


def get_invoices(db: Session):
    return db.query(models.Invoice).all()


def create_invoice(db: Session, invoice: invoice.InvoiceCreate):
    db_invoice = models.Invoice(
        amount=invoice.amount,
        date=invoice.date,
        profit=invoice.profit,
        customer_id=invoice.customer_id,
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def create_invoice_items(
    db: Session, invoice: invoice.InvoiceCreate, invoice_id_int: int
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
            )
        )

    # db.add_all(invoice.invoice_items)
    db.commit()

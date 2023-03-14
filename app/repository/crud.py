from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,status

from ..models import models

from ..schemas import customer,invoice,invoiceitem,product,productcategory,productimage,productitem,purchase,purchaseexpense,purchaseitem,supplier


def get_invoice(db: Session,id : int):
    return db.query(models.Invoice).filter(models.Invoice.id == id).first()

def get_invoices(db: Session):
    return db.query(models.Invoice).all()

def get_customers(db: Session):
    return db.query(models.Customer).all()

def create_customer(db: Session, user: customer.CreateCustomer):
    db_customer = models.Customer(name=user.name,mobile=user.mobile,address=user.address)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer_by_mobile(db: Session, mobile: int):
    return db.query(models.Customer).filter(models.Customer.mobile == mobile).first()

def delete_customer(db: Session,id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == id)

    if not customer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no customer exists with id - {id} ")

    customer.delete(synchronize_session=False)
    db.commit()
    return 'done'


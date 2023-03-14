from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .models import models

from .repository import crud

from .schemas import customer,invoice,invoiceitem,product,productcategory,productimage,productitem,purchase,purchaseexpense,purchaseitem,supplier

from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/invoices/", response_model=list[invoice.Invoice])
def read_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    invoices = crud.get_invoices(db)
    return invoices

@app.post("/customers/", response_model=customer.CustomerBase)
def create_customer(user: customer.CreateCustomer, db: Session = Depends(get_db)):
    db_user = crud.get_customer_by_mobile(db,user.mobile)

    if db_user:
        raise HTTPException(status_code=400, detail="Mobile already registered")
    return crud.create_customer(db=db, user=user)

@app.get("/customers/", response_model=list[customer.CustomerBase])
def read_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db=db)

@app.delete("/customers/")
def delete_customer(id: int,db: Session = Depends(get_db)):

    deleted = crud.delete_customer(db=db,id=id)
    if deleted:
        return {"status":"deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
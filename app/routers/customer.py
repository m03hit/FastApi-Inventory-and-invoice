from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import customer, invoice, invoiceitem, product, productcategory, productimage, productitem, purchase, purchaseexpense, purchaseitem, supplier
from ..repository import crud

router = APIRouter(
    prefix="/customers",
    tags=['Customer']
)


@router.post("/", response_model=customer.CustomerBase)
def create_customer(user: customer.CreateCustomer, db: Session = Depends(get_db)):
    db_user = crud.get_customer_by_mobile(db,user.mobile)

    if db_user:
        raise HTTPException(status_code=400, detail="Mobile already registered")
    return crud.create_customer(db=db, user=user)

@router.get("/", response_model=list[customer.CustomerBase])
def read_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db=db)

@router.delete("/")
def delete_customer(id: int,db: Session = Depends(get_db)):

    deleted = crud.delete_customer(db=db,id=id)
    if deleted:
        return {"status":"deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import customer, invoice, invoiceitem, product, productcategory, productimage, productitem, purchase, purchaseexpense, purchaseitem, supplier
from ..repository import crud

router = APIRouter(
    prefix="/invoices",
    tags=['Invoice']
)


#@router.post("/", status_code=status.HTTP_201_CREATED, response_model=customer.UserOut)
#def create_user(user: customer.UserCreate, db: Session = Depends(get_db)):
#    pass


@router.get("/", response_model=list[invoice.Invoice])
def read_invoices(db: Session = Depends(get_db)):
    invoices = crud.get_invoices(db)
    return invoices

@router.get("/{id}", response_model=invoice.Invoice)
def read_invoices(id: int,db: Session = Depends(get_db)):
    invoice = crud.get_invoice(db,id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no invoice found with the given id {id}")
    return invoice
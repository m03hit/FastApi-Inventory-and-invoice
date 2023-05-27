from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..repository import crud
from ..schemas import customer

router = APIRouter(prefix="/customers", tags=["Customer"])


@router.post(
    "/", response_model=customer.CustomerBase, status_code=status.HTTP_201_CREATED
)
def create_customer(user: customer.CreateCustomer, db: Session = Depends(get_db)):
    db_user = crud.get_customer_by_mobile(db, user.mobile)

    if db_user:
        raise HTTPException(
            status_code=400,
            detail=f"Mobile already registered with customer id {db_user.id}",
        )
    return crud.create_customer(db=db, user=user)


@router.get("/{id}", response_model=customer.CustomerBase)
def read_customer(id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, id)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no customer found with the given {id} ",
        )

    return db_customer


@router.get("/", response_model=list[customer.CustomerBase])
def read_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db=db)


""" @router.delete("/{id}")
def delete_customer(id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_customer(db=db, id=id)
    if deleted:
        return {"status": "deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) """

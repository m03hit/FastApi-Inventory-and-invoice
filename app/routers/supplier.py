from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..repository import crud
from ..schemas import supplier
from ..models import models
from ..repository import crud

router = APIRouter(prefix="/suppliers", tags=["Supplier"])


@router.post(
    "/", response_model=supplier.SupplierBase, status_code=status.HTTP_201_CREATED
)
def create_supplier(supplier: supplier.Supplier, db: Session = Depends(get_db)):
    existing_supplier = crud.get_supplier_by_mobile_no(supplier.mobile, db)
    if existing_supplier:
        raise HTTPException(
            status_code=409,
            detail=f"Supplier already exists with mobile number {supplier.mobile}",
        )
    created_supplier = crud.create_supplier(supplier, db)

    if not created_supplier:
        raise HTTPException(status_code=500, detail="Something went wrong")
    return created_supplier


@router.get("/", response_model=list[supplier.Supplier])
def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


@router.get("/{id}", response_model=supplier.Supplier)
def get_supplier(id: int, db: Session = Depends(get_db)):
    supplier = crud.get_supplier(id, db)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no supplier found with the given id {id}",
        )
    return supplier

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..repository import crud
from ..schemas import supplier
from ..models import models

router = APIRouter(prefix="/suppliers", tags=["Supplier"])


@router.post("/", response_model=supplier.SupplierBase)
def create_supplier(supplier: supplier.SupplierCreate, db: Session = Depends(get_db)):
    create_supplier = models.Supplier(name=supplier.name, mobile=supplier.mobile)
    db.add(create_supplier)
    db.commit()
    db.refresh(create_supplier)
    return create_supplier


@router.get("/", response_model=list[supplier.Supplier])
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(models.Supplier).all()


@router.get("/{id}", response_model=supplier.Supplier)
def get_supplier(id: int, db: Session = Depends(get_db)):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no supplier found with the given id {id}",
        )
    return supplier

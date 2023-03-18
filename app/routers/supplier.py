from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..repository import crud
from ..schemas import supplier
from ..models import models

router = APIRouter(
    prefix="/suppliers",
    tags=['Supplier']
)


@router.post("/", response_model=supplier.SupplierBase)
def create_supplier(supplier: supplier.SupplierCreate, db: Session = Depends(get_db)):
    create_supplier = models.Supplier(name=supplier.name, mobile=supplier.mobile)
    db.add(create_supplier)
    db.commit()
    db.refresh(create_supplier)
    return create_supplier

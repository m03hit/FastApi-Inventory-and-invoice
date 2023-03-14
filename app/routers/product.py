from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..repository import crud
from ..schemas import product
from ..models import models
router = APIRouter(
    prefix="/products",
    tags=['Product']
)

@router.post("/", response_model=product.ProductCreated)
def create_product(product: product.ProductCreate,db: Session = Depends(get_db)):
    product_to_add = models.Product(**product.dict())
    db.add(product_to_add)
    db.commit()
    db.refresh(product_to_add)
    return product_to_add


@router.get("/",response_model=list[product.Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()
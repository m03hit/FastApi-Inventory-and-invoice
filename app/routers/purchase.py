from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..repository import crud
from ..schemas import productcategory
from ..models import models
router = APIRouter(
    prefix="/productcategories",
    tags=['Product Category']
)

@router.post("/", response_model=productcategory.ProductCategoryBase)
def create_product_category(category: productcategory.ProductCategoryCreate,db: Session = Depends(get_db)):
    p_category = models.ProductCategory(name=category.name)
    db.add(p_category)
    db.commit()
    db.refresh(p_category)
    return p_category
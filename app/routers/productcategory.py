from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models
from ..schemas import productcategory

router = APIRouter(
    prefix="/productcategories",
    tags=['Product Category']
)


@router.post("/", response_model=productcategory.ProductCategoryBase)
def create_product_category(category: productcategory.ProductCategoryCreate, db: Session = Depends(get_db)):
    p_category = models.ProductCategory(name=category.name)
    db.add(p_category)
    db.commit()
    db.refresh(p_category)
    return p_category


@router.get("/", response_model=list[productcategory.ProductCategory])
def get_product_categories(db: Session = Depends(get_db)):
    return db.query(models.ProductCategory).all()

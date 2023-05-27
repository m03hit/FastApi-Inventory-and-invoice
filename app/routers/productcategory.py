from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models
from ..schemas import productcategory

router = APIRouter(prefix="/productcategories", tags=["Product Category"])


@router.post("/", response_model=productcategory.ProductCategoryBase)
def create_product_category(
    category: productcategory.ProductCategoryCreate, db: Session = Depends(get_db)
):
    p_category = models.ProductCategory(name=category.name)
    db.add(p_category)
    db.commit()
    db.refresh(p_category)
    return p_category


@router.get("/", response_model=list[productcategory.ProductCategory])
def get_product_categories(db: Session = Depends(get_db)):
    return db.query(models.ProductCategory).all()


@router.get("/{id}", response_model=productcategory.ProductCategory)
def get_product_categorie(id: int, db: Session = Depends(get_db)):
    product_category = (
        db.query(models.ProductCategory).filter(models.ProductCategory.id == id).first()
    )
    if not product_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no product Catergory found with the given id {id}",
        )
    return product_category

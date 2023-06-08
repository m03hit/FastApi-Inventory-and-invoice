from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models
from ..schemas import productcategory
from ..repository import crud

router = APIRouter(prefix="/productcategories", tags=["Product Category"])


@router.post(
    "/",
    response_model=productcategory.ProductCategory,
    status_code=status.HTTP_201_CREATED,
)
def create_product_category(
    category: productcategory.ProductCategoryBase, db: Session = Depends(get_db)
):
    product_category = crud.create_category(db, category)
    if product_category.id > 0:
        return product_category
    else:
        raise HTTPException(
            status_code=500, detail="Something went wrong, please try again or contact "
        )


@router.get("/", response_model=list[productcategory.ProductCategory])
def get_product_categories(db: Session = Depends(get_db)):
    return crud.get_product_categories(db)


@router.get("/{id}", response_model=productcategory.ProductCategoryWithProducts)
def get_product_category(id: int, db: Session = Depends(get_db)):
    product_category = crud.get_product_category(id, db)

    if product_category == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no product Catergory found with the given id {id}",
        )
    return product_category

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models import models
from ..schemas import productimage
from ..repository import crud

router = APIRouter(prefix="/productimages", tags=["Product Image"])


@router.post("/", response_model=productimage.ProductImage)
def create_product_image(
    product_image: productimage.ProductImageBase, db: Session = Depends(get_db)
):
    product_exists_or_not = crud.read_product(product_image.product_id, db)
    if not product_exists_or_not:
        raise HTTPException(
            status_code=404,
            detail=f"no product found with id {product_image.product_id}",
        )
    image_to_be_created = crud.create_image(
        product_image.product_id, db, product_image.image_url
    )
    if not image_to_be_created:
        raise HTTPException(
            status_code=500, detail="Something went wrong,please try again"
        )
    return image_to_be_created


@router.get("/{id}", response_model=productimage.ProductImage)
def get_product_image(id: int, db: Session = Depends(get_db)):
    product_image = crud.read_image(id, db)
    if not product_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no product image found with the given id {id}",
        )
    return product_image


@router.get("/", response_model=list[productimage.ProductImage])
def get_product_images(db: Session = Depends(get_db)):
    return crud.read_images(db)

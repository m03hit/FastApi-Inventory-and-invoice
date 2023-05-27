from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models import models
from ..schemas import productimage

router = APIRouter(prefix="/productimages", tags=["Product Image"])


@router.post("/", response_model=productimage.ProductImageCreated)
def create_product_image(
    product_image: productimage.ProductImageCreate, db: Session = Depends(get_db)
):
    image = models.ProductImage(
        image_url=product_image.image_url, product_id=product_image.product_id
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


@router.get("/{id}", response_model=productimage.ProductImage)
def get_product_image(id: int, db: Session = Depends(get_db)):
    product_image = (
        db.query(models.ProductImage).filter(models.ProductImage.id == id).first()
    )

    if not product_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no product image found with the given id {id}",
        )
    return product_image


@router.get("/", response_model=list[productimage.ProductImage])
def get_product_images(db: Session = Depends(get_db)):
    return db.query(models.ProductImage).all()

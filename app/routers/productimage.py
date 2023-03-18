from fastapi import Depends, APIRouter
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

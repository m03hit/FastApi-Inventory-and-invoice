from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..repository import crud
from ..schemas import productimage
from ..models import models
router = APIRouter(
    prefix="/productimages",
    tags=['Product Image']
)

@router.post("/", response_model=productimage.ProductImageCreated)
def create_product_image(product_image: productimage.ProductImageCreate,db: Session = Depends(get_db)):
    image = models.ProductImage(image_url=product_image.image_url,product_id=product_image.product_id)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image
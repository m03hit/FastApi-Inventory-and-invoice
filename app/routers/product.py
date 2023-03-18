from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models import models
from ..schemas import product

router = APIRouter(
    prefix="/products",
    tags=['Product']
)


@router.post("/", response_model=product.ProductCreated)
def create_product(product: product.ProductCreate, db: Session = Depends(get_db)):
    product_to_add = models.Product(name=product.name, measure_unit=product.measure_unit,
                                    selling_unit=product.selling_unit, category_id=product.category_id)
    db.add(product_to_add)
    db.commit()
    db.refresh(product_to_add)
    for image in product.product_images:
        db.add(models.ProductImage(image_url=image, product_id=product_to_add.id))
        db.commit()
    return db.query(models.Product).filter(models.Product.id == product_to_add.id).first()


@router.get("/", response_model=list[product.Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

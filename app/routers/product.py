from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models import models
from ..schemas import product
from ..schemas.product import MeasurementUnitEnum

router = APIRouter(prefix="/products", tags=["Product"])


@router.post("/", response_model=product.ProductCreated, status_code=201)
def create_product(product: product.ProductCreate, db: Session = Depends(get_db)):
    product_to_add = models.Product(
        name=product.name,
        measurement_unit=product.measurement_unit,
        category_id=product.category_id,
    )
    db.add(product_to_add)
    db.commit()
    db.refresh(product_to_add)
    for image in product.product_images:
        db.add(models.ProductImage(image_url=image, product_id=product_to_add.id))
        db.commit()
    return (
        db.query(models.Product).filter(models.Product.id == product_to_add.id).first()
    )


@router.get("/", response_model=list[product.ProductWithoutProductItems])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@router.get("/{id}", response_model=product.ProductWithProductItems)
def read_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no product found with the given id {id}",
        )
    return product

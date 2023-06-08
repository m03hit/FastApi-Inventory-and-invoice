from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models import models
from ..schemas import product
from ..schemas.baseSchema import MeasurementUnitEnum
from ..repository import crud

router = APIRouter(prefix="/products", tags=["Product"])


@router.post("/", response_model=product.Product, status_code=201)
def create_product(product: product.ProductCreate, db: Session = Depends(get_db)):
    if crud.does_category_exists(db, product.category_id) == False:
        raise HTTPException(
            status_code=422,
            detail=f"no category exists with category id : {product.category_id}",
        )

    if crud.does_measurement_way_exists(db, product.measurement_way_id) == False:
        raise HTTPException(
            status_code=422,
            detail=f"no measurement way exists with id : {product.measurement_way_id}",
        )

    product_to_add = crud.create_product(product, db)
    if product_to_add is None:
        raise HTTPException(
            status_code=500, detail="Some error occurred while adding product"
        )
    for image_url in product.product_images:
        image_created = crud.create_image(product_to_add.id, db, image_url)
        if image_created == None:
            raise HTTPException(
                status_code=500, detail="Some error occurred while adding product photo"
            )

    product_to_return = crud.read_product(product_to_add.id, db)
    if product_to_return is not None:
        return product_to_add
    else:
        raise HTTPException(
            status_code=500, detail="Some error occurred while adding product"
        )


@router.get("/", response_model=list[product.ProductWithProductImages])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@router.get("/{id}", response_model=product.ProductWithProductItems)
def read_product(id: int, db: Session = Depends(get_db)):
    product = crud.read_product(id, db)
    if product == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no product found with the given id {id}",
        )
    return product

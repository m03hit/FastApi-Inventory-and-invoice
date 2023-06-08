from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models
from ..schemas import purchase, baseSchema
from ..repository import crud


router = APIRouter(prefix="/purchases", tags=["Product Purchase"])


@router.post("/", response_model=purchase.Purchase, status_code=status.HTTP_201_CREATED)
def create_purchase(purchase: purchase.PurchaseCreate, db: Session = Depends(get_db)):
    supplier = crud.get_supplier(purchase.supplier_id, db)

    if not supplier:
        raise HTTPException(
            status_code=404,
            detail=f"""no supplier exists with id {purchase.supplier_id} ,please add a new supplier before proceeding forward""",
        )

    for product_item in purchase.products:
        product_exists_or_not = crud.read_product(product_item.product_id, db)
        if not product_exists_or_not:
            raise HTTPException(
                status_code=404,
                detail=f"""no product found with id {product_item.product_id}, please add the product first """,
            )

    base_purchase = purchase
    added_Purchase = models.Purchase(
        date=purchase.date,
        title=purchase.title,
        amount=purchase.amount,
        supplier_id=purchase.supplier_id,
    )
    db.add(added_Purchase)
    db.commit()
    db.refresh(added_Purchase)
    for expense in base_purchase.purchase_expenses:
        db.add(
            models.PurchaseExpense(
                amount=expense.amount,
                title=expense.title,
                description=expense.description,
                purchase_id=added_Purchase.id,
            )
        )
        db.commit()

    for product_item in base_purchase.products:
        db.add(
            models.ProductItem(
                unit_price=product_item.unit_price,
                effective_unit_price=product_item.effective_unit_price,
                quantity=product_item.quantity,
                product_id=product_item.product_id,
                purchase_id=added_Purchase.id,
                total_value=(product_item.effective_unit_price * product_item.quantity),
            )
        )
        db.commit()
    return (
        db.query(models.Purchase)
        .filter(models.Purchase.id == added_Purchase.id)
        .first()
    )


@router.get("/{id}", response_model=purchase.PurchaseWithProductsAndExpenses)
def read_purchase(id: int, db: Session = Depends(get_db)):
    purchase = crud.read_purchase(id, db)
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no purchase found with the given id {id}",
        )
    return purchase


@router.get("/", response_model=list[purchase.Purchase])
def read_purchases(db: Session = Depends(get_db)):
    return crud.read_purchases(db)

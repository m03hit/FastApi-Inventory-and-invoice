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

    if len(purchase.products):
        raise HTTPException(
            status_code=422, detail="can't create purchase without any product/s"
        )

    added_Purchase = crud.create_purchase(purchase, db)
    if not added_Purchase:
        raise HTTPException(
            status_code=500, detail="Something went wrong, Please Try again"
        )
    crud.create_purchase_expenses(added_Purchase.id, purchase.purchase_expenses, db)
    # for expense in base_purchase.purchase_expenses:
    #     db.add(
    #         models.PurchaseExpense(
    #             amount=expense.amount,
    #             title=expense.title,
    #             description=expense.description,
    #             purchase_id=added_Purchase.id,
    #         )
    #     )
    #     db.commit()
    crud.create_product_items(purchase.products, added_Purchase.id, db)
    # for product_item in base_purchase.products:
    #     db.add(
    #         models.ProductItem(
    #             unit_price=product_item.unit_price,
    #             effective_unit_price=product_item.effective_unit_price,
    #             quantity=product_item.quantity,
    #             product_id=product_item.product_id,
    #             purchase_id=added_Purchase.id,
    #             total_value=(product_item.effective_unit_price * product_item.quantity),
    #         )
    #     )
    #     db.commit()
    return crud.read_purchase(added_Purchase.id, db)


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

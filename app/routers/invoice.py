from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..schemas import invoice, invoiceitem, productitem
from ..repository import crud
from ..models import models

router = APIRouter(prefix="/invoices", tags=["Invoice"])


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=customer.UserOut)
# def create_user(user: customer.UserCreate, db: Session = Depends(get_db)):
#    pass


@router.get("/", response_model=list[invoice.Invoice])
def read_invoices(db: Session = Depends(get_db)):
    invoices = crud.get_invoices(db)
    return invoices


@router.get("/{id}", response_model=invoice.InvoiceWithInvoiceItems)
def read_invoice(id: int, db: Session = Depends(get_db)):
    invoice = crud.get_invoice(db, id)
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no invoice found with the given id {id}",
        )
    return invoice


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=invoice.Invoice)
# def create_invoice(invoice: invoice.InvoiceCreate, db: Session = Depends(get_db)):
#     customer = crud.get_customer(db, invoice.customer_id)
#     if not customer:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"customer with id {invoice.customer_id} does not exist",
#         )
#     for product in invoice.invoice_items:
#         product_exists_or_not = crud.read_product(product.product_id, db)
#         if not product_exists_or_not:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"no product exists with product id {product.product_id}",
#             )
#         if product_exists_or_not.total_quantity < product.quantity:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"There is not enought stock of product id {product.product_id}",
#             )
#     invoice_created = crud.create_invoice(db, invoice)
#     crud.create_invoice_items(db, invoice, invoice_created.id)
#     return crud.get_invoice(db, invoice_created.id)

#     # for product in invoice.invoice_items:
#     #     quantity = crud.get_total_quantity_of_product(product.product_id, db)
#     #     print(quantity)
#     #     if quantity < product.quantity:
#     #         raise HTTPException(
#     #             status_code=404,
#     #             detail=f"There is not enought stock of product id {product.product_id}",
#     #         )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=invoice.Invoice)
def create_invoice(invoice: invoice.InvoiceCreate, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, invoice.customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {invoice.customer_id} does not exist",
        )

    for product in invoice.invoice_items:
        product_exists = crud.read_product(product.product_id, db)
        if not product_exists:
            raise HTTPException(
                status_code=404,
                detail=f"No product exists with product id {product.product_id}",
            )
    # for product in invoice.invoice_items:
    #    quantity_query = crud.get_total_quantity_of_product(product.product_id, db)
    #    if quantity_query < product.quantity:
    #        raise HTTPException(
    #            status_code=409,
    #            detail=f"There is not enought stock of product id {product.product_id}",
    #        )

    # niche vaala fix karde
    # unique_product_id_with_quantity = []

    # for product in invoice.invoice_items:
    #     for item in unique_product_id_with_quantity:
    #         if item.product_id == product.product_id:
    #             item.quantity = item.quantity + product.quantity
    #         else:
    #             unique_product_id_with_quantity.add(
    #                 invoiceitem.InvoiceItemBase(
    #                     product_id=product.product_id,
    #                     quantity=product.quantity,
    #                     amount=0,
    #                     unit_price=0,
    #                 )
    #             )

    # print(unique_product_id_with_quantity)

    unique_product_id_with_quantity = []

    for product in invoice.invoice_items:
        found = False
        for item in unique_product_id_with_quantity:
            if item.product_id == product.product_id:
                item.quantity += product.quantity
                found = True
                break
        if not found:
            unique_product_id_with_quantity.append(
                invoiceitem.InvoiceItemBase(
                    product_id=product.product_id,
                    quantity=product.quantity,
                    amount=0,
                    unit_price=0,
                )
            )

    for product in unique_product_id_with_quantity:
        quantity_query = crud.get_total_quantity_of_product(product.product_id, db)
        if quantity_query < product.quantity:
            raise HTTPException(
                status_code=409,
                detail=f"There is not enought stock of product id {product.product_id}",
            )

    # upar vaala fix karde
    invoice_items = []
    # update amount and profit after adding items
    # this won't probably work with granites, individual items
    # maybe merge duplicate invoice_items first or handle total quantity before commiting
    for product in invoice.invoice_items:
        remaining_quantity = product.quantity
        # should be recieved in the order of date
        product_items = crud.read_product_items_by_p_id(product.product_id, db)
        for product_item in product_items:
            if remaining_quantity > 0:
                if product_item.quantity >= remaining_quantity:
                    # Create invoice item with the oldest product item
                    invoice_item = models.InvoiceItem(
                        amount=0,  # fix it later
                        product_id=product.product_id,
                        invoice_id=None,  # Will be assigned later
                        product_item_id=product_item.id,
                        quantity=remaining_quantity,
                        unit_price=product_item.unit_price,
                    )
                    invoice_items.append(invoice_item)
                    remaining_quantity = 0
                else:
                    # Create invoice item with the full quantity of the current product item
                    invoice_item = models.InvoiceItem(
                        amount=0,  # fix it later
                        product_id=product.product_id,
                        invoice_id=None,  # Will be assigned later
                        product_item_id=product_item.id,
                        quantity=product_item.quantity,
                        unit_price=product_item.unit_price,
                    )
                    if invoice_item.quantity > 0:
                        invoice_items.append(invoice_item)
                        remaining_quantity -= product_item.quantity
        if remaining_quantity > 0:
            raise HTTPException(
                status_code=404,
                detail=f"Not enough stock of product id {product.product_id}",
            )

    invoice_created = crud.create_invoice(db, invoice)
    for item in invoice_items:
        item.invoice_id = invoice_created.id
        item.amount = item.unit_price * item.quantity
    crud.create_invoice_items(db, invoice_items)
    pid_list = []
    for product in invoice.invoice_items:
        pid_list.append(product.product_id)
    crud.update_total_quantity(pid_list, db)
    crud.update_total_value_in_product_and_items(db)
    # Assign the invoice ID to the invoice items
    # for invoice_item in invoice_items:
    #     crud.update_invoice_item_invoice_id(db, invoice_item.id, invoice_created.id)

    return crud.get_invoice(db, invoice_created.id)

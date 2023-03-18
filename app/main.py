from fastapi import FastAPI

from .database.database import engine
from .models import models
from .routers import (
    customer,
    invoice,
    productcategory,
    product,
    productimage,
    supplier,
    purchase,
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(customer.router)
app.include_router(invoice.router)
app.include_router(productcategory.router)
app.include_router(product.router)
app.include_router(productimage.router)
app.include_router(supplier.router)
app.include_router(purchase.router)

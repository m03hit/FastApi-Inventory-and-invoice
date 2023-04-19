from fastapi import FastAPI, Depends
from . import oauth2
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
    auth,
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_customers(current_user: int = Depends(oauth2.get_current_user)):
    return "it works"


app.include_router(customer.router)
app.include_router(invoice.router)
app.include_router(productcategory.router)
app.include_router(product.router)
app.include_router(productimage.router)
app.include_router(supplier.router)
app.include_router(purchase.router)
app.include_router(auth.router)

from fastapi import Depends, FastAPI, HTTPException, status

from .models import models
from .routers import customer, invoice, productcategory, product, productimage, supplier


from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(customer.router)
app.include_router(invoice.router)
app.include_router(productcategory.router)
app.include_router(product.router)
app.include_router(productimage.router)
app.include_router(supplier.router)

from fastapi import Depends, FastAPI, HTTPException, status

from .models import models
from .routers import customer,invoice


from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(customer.router)
app.include_router(invoice.router)

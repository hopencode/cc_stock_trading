from fastapi import FastAPI


from app.routers import customer_router
from app.routers import admin_router



app = FastAPI()

app.include_router(admin_router.router)
app.include_router(customer_router.router)
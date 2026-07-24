from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.role import router as role_router
from app.routers.users import router as users_router
from app.routers.supplier import router as supplier_router
from app.routers.product import router as product_router
from app.routers.ingredient import router as ingredient_router
from app.routers.purchase import router as purchase_router


app = FastAPI(title="BakeryOS API")

app.include_router(role_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(supplier_router)
app.include_router(product_router)
app.include_router(ingredient_router)
app.include_router(purchase_router)


@app.get("/")
def root():
    return {"message": "Welcome to BakeryOS"}
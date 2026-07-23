from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.role import router as role_router
from app.routers.users import router as users_router

app = FastAPI(title="BakeryOS API")

app.include_router(role_router)
app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "Welcome to BakeryOS"}
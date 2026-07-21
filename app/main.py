from fastapi import FastAPI
from app.routers.role import router as role_router

app = FastAPI(title="BakeryOS API")

app.include_router(role_router)


@app.get("/")
def root():
    return {"message": "Welcome to BakeryOS "}
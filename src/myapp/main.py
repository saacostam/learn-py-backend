from fastapi import FastAPI

from myapp.features.presentation import user_router

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"Hello": "World"}

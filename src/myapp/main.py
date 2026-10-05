from fastapi import FastAPI

from myapp.features.todo.presentation import todo_router
from myapp.features.user.presentation import user_router

app = FastAPI()

app.include_router(todo_router, prefix="/todos", tags=["todos"])
app.include_router(user_router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"Hello": "World"}

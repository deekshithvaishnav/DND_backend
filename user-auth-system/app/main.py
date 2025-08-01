from fastapi import FastAPI
from . import models
from .database import engine
from app.routers.users import router as user_router
from app.routers import session
from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router 



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(session.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the login system!"}
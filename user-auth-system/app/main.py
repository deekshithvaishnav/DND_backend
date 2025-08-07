from fastapi import FastAPI
from . import models
from .database import engine
from app.routers.users import router as user_router
from app.routers import session
from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router 
from app.routers import auth, officer, supervisor, operator, notifications  # <- make sure to import
from app.routers import users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(session.router)

# backend/app/main.py
app = FastAPI()

app.include_router(auth.router)
app.include_router(officer.router)
app.include_router(supervisor.router)
app.include_router(operator.router)
app.include_router(notifications.router)
app.include_router(users.router)  # <- add this


@app.get("/")
def read_root():
    return {"message": "Welcome to the login system!"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend dev URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# backend/app/main.py
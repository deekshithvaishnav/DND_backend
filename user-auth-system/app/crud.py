from sqlalchemy.orm import Session
from . import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEFAULT_PASSWORD = "12345678"  # Default password for new users

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, username: str, role: str):
    hashed_password = get_password_hash(DEFAULT_PASSWORD)
    db_user = models.User(username=username, hashed_password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.services.auth_service import create_access_token, get_current_user, get_password_hash, verify_password
from app.core.models.user import User
from app.adapters.repositories.base import SessionLocal
import logging

from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)


class UserRegister(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: UserRegister):
    db = SessionLocal()
    logger.info(f"Registering user: {user.username}")
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}


class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(user: UserLogin):
    db = SessionLocal()
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/check_token")
def check_token(current_user: User = Depends(get_current_user)):
    logger.info(f"Token check for user: {current_user.username}")
    return {"message": "Token is valid"}
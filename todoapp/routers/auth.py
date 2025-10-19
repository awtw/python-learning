from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, oauth2
from jose import JWTError, jwt

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = "09ec212c94f7a36694c102c4453594b705b6b63b7e570595c1533819cacc8ba6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str = "user"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/")
async def get_user():
    return {"user": "authenticated"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(db: db_dependency, user_request: UserRequest):
    if db.query(Users).filter(Users.username == user_request.username).first() is not None:
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(Users).filter(Users.email == user_request.email).first() is not None:
        raise HTTPException(status_code=400, detail="Email already exists")
    create_user_model = Users(
        username=user_request.username,
        email=user_request.email,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=bcrypt_context.hash(user_request.password),
        role=user_request.role
    )
    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}

# @router.post("/auth/login", status_code=status.HTTP_200_OK)
# async def login_for_access_token(db: db_dependency, user_request: UserRequest):
#     user = authenticate_user(db, user_request.username, user_request.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token = create_access_token(user.id)
#     return {"access_token": token, "token_type": "bearer"}

@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": create_access_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)), "token_type": "bearer"}


def authenticate_user(db: db_dependency, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
from typing import Annotated, Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict
from sqlalchemy.orm import Session
from fastapi import APIRouter, FastAPI, Depends, HTTPException, Path, status 
from models import Todos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todo", status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency, user: user_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    query = db.query(Todos).filter(Todos.valid_flag == True)
    return query.all()
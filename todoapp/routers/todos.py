from typing import Annotated, Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict
from sqlalchemy.orm import Session
from fastapi import APIRouter, FastAPI, Depends, HTTPException, Path 
from models import Todos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    priority: int = Field(gt=0, lt=6)   
    complete: bool = False
    # valid_flag: Optional[bool] = None


class TodoResponse(BaseModel):
    # Map from ORM object to Pydantic model
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    priority: int
    complete: bool

@router.get("/", response_model=list[TodoResponse])
async def read_todos(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    query = db.query(Todos).filter(Todos.valid_flag == True).filter(Todos.owner_id == user.get("id"))
    return query.all()

@router.get("/{todo_id}", response_model=TodoResponse)
async def read_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(..., gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.valid_flag == True).filter(Todos.owner_id == user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

@router.post("/", response_model=TodoResponse)
async def create_todo(db: db_dependency, todo_request: TodoRequest, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo_model = Todos(**todo_request.model_dump(exclude_unset=True), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(db: db_dependency, todo_request: TodoRequest, user: user_dependency, todo_id: int = Path(..., gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first().filter(Todos.owner_id == user.get("id"))    
    if todo_model is not None:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete
        db.commit()
        db.refresh(todo_model)
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/{todo_id}")
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(..., gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.valid_flag == True).filter(Todos.owner_id == user.get("id")).first()
    if todo_model is not None:
        todo_model.valid_flag = False
        db.commit()
        return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
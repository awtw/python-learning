from itertools import count
from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from starlette import status

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
    rating: int

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    category: str = Field(min_length=1)
    rating: int = Field(gt=0, lt=6)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Title One",
                "author": "Author One",
                "category": "science",
                "rating": 5,
            }
        }
    )

BOOKS: list[Book] = [
    Book(id=1, title='Title One', author='Author One', category='science', rating=5),
    Book(id=2, title='Title Two', author='Author Two', category='science', rating=5),
    Book(id=3, title='Title Three', author='Author Three', category='history', rating=5),
    Book(id=4, title='Title Four', author='Author Four', category='math', rating=5),
    Book(id=5, title='Title Five', author='Author Five', category='math', rating=5),
    Book(id=6, title='Title Six', author='Author Two', category='math', rating=5)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(description="The ID of the book to get", gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.get("/books/Rating", status_code=status.HTTP_200_OK)
async def get_books_by_rating(rate: int = Query(description="The rating to filter by", gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating >= rate:
            books_to_return.append(book)
    return books_to_return

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    data = book_request.model_dump(exclude={"id"}, exclude_none=True)
    new_book = Book(id=next_book_id(), **data)
    BOOKS.append(new_book)
    return new_book

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest):
    book_change = False
    for idx, book in enumerate(BOOKS):
        if book.id == book_request.id:
            BOOKS[idx] = Book(**book_request.model_dump())
            book_change = True
            break
    if not book_change:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(description="The ID of the book to delete", gt=0)):
    book_change = False
    for idx, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(idx)
            book_change = True
            break
    if not book_change:
        raise HTTPException(status_code=404, detail="Book not found")

# def find_book_index(book: Book):
#     book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
#     return book

# 從現有最大 id + 1 開始（刪除造成的缺口無妨）
# id_counter = count(start=max((b.id for b in BOOKS), default=0) + 1)

@app.get("/__debug/versions")
def versions():
    import pydantic, fastapi
    from pydantic import BaseModel
    return {
        "pydantic": pydantic.__version__,
        "fastapi": fastapi.__version__,
        "base_model_module": BaseModel.__module__,  # 若顯示 'pydantic.v1' 代表你其實在用 v1 介面
    }

def next_book_id() -> int:
    return max((b.id for b in BOOKS), default=0) + 1
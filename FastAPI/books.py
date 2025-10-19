from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

class Book(BaseModel):
    title: str
    author: str
    category: str


@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return {"message": "Book not found"}

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            (book.get('author') or '').casefold() == book_author.casefold()
            and (book.get('category') or '').casefold() == category.casefold()
        ):
            books_to_return.append(book)
    if len(books_to_return) <= 0:
        return { "message": "No books found" }       
    return {"data": books_to_return}

@app.post(f"/books/create_book")
async def create_book(book_request: Book):
    BOOKS.append(book_request)
    return book_request

@app.put("/books/update_book")
async def update_book(book_request: Book):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_request.title.casefold():
            BOOKS[i] = book_request
            return BOOKS
    return {"message": "Book not found"}

@app.delete("/books/delete_book")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            return BOOKS
    return {"message": "Book not found"}
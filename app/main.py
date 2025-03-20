import uvicorn
from typing import Any
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import Book, get_db, drop_database_and_load_data, read_book
from app.schemas import BookSchema, BookSchemaCreate

app = FastAPI(description="Pre Employment Test Service")


@app.get("/book", response_model=list[BookSchema])
def list_book(db: Session = Depends(get_db)) -> Any:
    return db.query(Book).all()


@app.post("/book")
def create_book(data: BookSchemaCreate, db: Session = Depends(get_db)) -> BookSchema:
    book = Book(**data.model_dump())
    db.add(book)
    db.commit()

    return book


@app.get("/book/{book_id}")
def get_book(book: Book = Depends(read_book)) -> BookSchema:
    return book


@app.patch("/book/{book_id}")
def update_book(data: BookSchemaCreate, book: Book = Depends(read_book), db: Session = Depends(get_db)) -> BookSchema:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)

    return book


if __name__ == "__main__":
    drop_database_and_load_data()
    uvicorn.run("app.main:app", port=8080, reload=True, access_log=False)

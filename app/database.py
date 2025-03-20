import os
from faker import Faker
from fastapi import Depends, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Any, Generator
from rich import print

Base = declarative_base()
Faker.seed(42)

# Database setup
SQLITE_DB = "test.db"
DATABASE_URL = f"sqlite:///./{SQLITE_DB}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Book(Base):
    __tablename__ = "book"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, index=True)
    author: str = Column(String, index=True)


def get_db() -> Generator[Any, Any, Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_fixtures() -> None:
    # Generate fixtures
    print(f"[yellow]loading fixtures[/yellow]")
    faker = Faker()
    db = SessionLocal()
    for i in range(10):
        book = Book(id=i, name=faker.name(), author=faker.sentence(4))
        db.add(book)
        print(f"book: [blue]{book.id}[/blue] {book.name}")
    db.commit()
    db.close()
    print(f"[green]loading fixtures done[/green]")


# Parameter Converter (Dependency)
def read_book(book_id: int, db: Session = Depends(get_db)) -> Book:
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def drop_database_and_load_data() -> None:
    if os.path.exists(SQLITE_DB):
        os.unlink(SQLITE_DB)
    Base.metadata.create_all(bind=engine)
    load_fixtures()

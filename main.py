"""This is main module
"""

from datetime import date
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api.models import BookResponse, BookRequest

from db.database import get_db,Base,engine
from db.models import Books

# Create the database tables
Base.metadata.create_all(bind=engine)
app = FastAPI()

# We need to get db connection here
@app.get("/books", response_model=list[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    """This method gets all the books 
    """
    return db.query(Books).all()
    


@app.post("/books", response_model=BookResponse)
def create_book(request: BookRequest,db: Session = Depends(get_db)):
    """This method creates a book
    """
    db_book = Books(**request.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """This method gets a book
    """
    return db.query(Books).filter(Books.id == book_id).first()

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, request: BookRequest, db: Session = Depends(get_db)):
    """This method updates a book
    """
    db_book = db.query(Books).filter(Books.id == book_id).first()
    if db_book:
        db_book.title = request.title
        db_book.author = request.author
        db_book.isbn = request.isbn
        db_book.published_date = request.published_date
        db.commit()
        db.refresh(db_book)
    return db_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """This method deletes a book
    """
    db_book = db.query(Books).filter(Books.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return {"message": "Book deleted successfully"}


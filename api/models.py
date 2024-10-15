"""This module will have api models of the library
"""
from datetime import date
from pydantic import BaseModel, Field


class BookRequest(BaseModel):
    """This represent a request of Book
    """
    title: str = Field(
        ...,
        description="book title",
        example="Dopamine Detox")
    author: str = Field(
        ...,
        example="Thibaut Meurissee", 
        description="author")
    isbn: str
    published_date: date

class BookResponse(BaseModel):
    """This represents the response
    """
    id: int = Field(...,description="id",example="1")
    title: str = Field(...,description="book title",example="Dopamine Detox")
    author: str = Field(...,example="Thibaut Meurissee", description="author")
    isbn: str
    published_date: date
    class Config:
        orm_mode = True

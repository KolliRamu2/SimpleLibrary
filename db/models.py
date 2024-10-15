"""This module contains database models
"""

from sqlalchemy import  Column, Integer, String,Date
from db.database import Base

class Books(Base):
    """This represents the database table Books
    """
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    isbn = Column(String)
    published_date = Column(Date)

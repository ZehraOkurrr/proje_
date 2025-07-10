from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))  
    age = Column(Integer)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(255))
    price = Column(Integer)
    color = Column(String(50))
    quantity = Column(Integer)


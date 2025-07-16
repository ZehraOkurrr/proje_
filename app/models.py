from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(12))
    age = Column(Integer)

    # One-to-many ilişki (kullanıcının ürünleri olabilir)
    products = relationship("Product", back_populates="owner")

    # One-to-one ilişki (kullanıcının tek bir company’si olabilir)
    company = relationship("Company", back_populates="user", uselist=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(255))
    price = Column(Integer)
    color = Column(String(50))
    quantity = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)  # her company yalnızca 1 user ile ilişkili olabilir

    user = relationship("User", back_populates="company")

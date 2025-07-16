from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# -------------------- ASSOCIATION TABLE --------------------

product_category = Table(
    "product_category",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)

# -------------------- CATEGORY --------------------

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    products = relationship(
        "Product",
        secondary=product_category,
        back_populates="categories"
    )

# -------------------- USER --------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    age = Column(Integer)

    products = relationship("Product", back_populates="owner")
    company = relationship("Company", back_populates="user", uselist=False)

# -------------------- PRODUCT --------------------

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(255))
    price = Column(Integer)
    color = Column(String(50))
    quantity = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")

    categories = relationship(
        "Category",
        secondary=product_category,
        back_populates="products"
    )

# -------------------- COMPANY --------------------

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    user = relationship("User", back_populates="company")

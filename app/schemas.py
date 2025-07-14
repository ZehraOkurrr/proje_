from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

# -------------------- USER --------------------

class UserBase(BaseModel):
    name: str
    age: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }

# -------------------- PRODUCT --------------------

class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    color: str
    quantity: int

class ProductCreate(ProductBase):
    user_id: int

class Product(ProductBase):
    id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }

# -------------------- RESPONSE WRAPPER --------------------

T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    status: bool
    data: Optional[T] = None
    message: Optional[str] = None

    model_config = {
        "exclude_none": True
    }

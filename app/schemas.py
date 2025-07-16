from typing import TypeVar, Generic, Optional, List
from pydantic import BaseModel, root_validator, Field, validator
from pydantic.generics import GenericModel

# -------------------- CATEGORY --------------------

class CategoryBase(BaseModel):
    name: str = Field(..., max_length = 6)

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    model_config = {
        "from_attributes": True
    }

    @validator("name")
    def check_name_length(cls, value):
        if len(value) > 4:
            raise ValueError("Name must be at most 6 characters")
        return value

# -------------------- COMPANY --------------------

class CompanyBase(BaseModel):
    name: str = Field(..., max_length=4)

class CompanyCreate(CompanyBase):
    user_id: int

class Company(CompanyBase):
    id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }

    @validator("name")
    def check_name_length(cls, value):
        if len(value) > 4:
            raise ValueError("Name must be at most 4 characters")
        return value

# -------------------- USER --------------------

class UserBase(BaseModel):
    name: str = Field(..., max_length=4)
    age: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }

    @validator("name")
    def check_name_length(cls, value):
        if len(value) > 4:
            raise ValueError("Name must be at most 4 characters")
        return value

# -------------------- PRODUCT --------------------

class ProductBase(BaseModel):
    name: str = Field(..., max_length=4)
    description: str
    price: int
    color: str
    quantity: int

class ProductCreate(ProductBase):
    user_id: int
    category_ids: Optional[List[int]] = []

class Product(ProductBase):
    id: int
    user_id: int
    categories: Optional[List[Category]] = []

    model_config = {
        "from_attributes": True
    }

    @validator("name")
    def check_name_length(cls, value):
        if len(value) > 4:
            raise ValueError("Name must be at most 4 characters")
        return value

# -------------------- RESPONSE WRAPPER --------------------

T = TypeVar("T")

class ResponseModel(GenericModel, Generic[T]):
    status: bool
    data: Optional[T] = None
    message: Optional[str] = None

    @root_validator(pre=True)
    def _hide_fields(cls, values):
        if values.get("status") is True:
            values.pop("message", None)
        else:
            values.pop("data", None)
        return values

    @classmethod
    def success(cls, data: T):
        return cls(status=True, data=data)

    @classmethod
    def error(cls, message: str):
        return cls(status=False, message=message)

    model_config = {
        "exclude_none": True
    }

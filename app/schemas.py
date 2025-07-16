from typing import TypeVar, Generic, Optional, List
from pydantic import BaseModel, root_validator
from pydantic.generics import GenericModel

# -------------------- COMPANY --------------------

class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    user_id: int

class Company(CompanyBase):
    id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }

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
        "json_encoders": {},
        "exclude_none": True  # <<< işte bu satır!
    }

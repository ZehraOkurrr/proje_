from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    age: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True  


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    color: str
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True  



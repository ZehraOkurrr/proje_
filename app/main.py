from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Users

@app.post("/users/", response_model=schemas.ResponseModel)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    created = crud.create_user(db, user)
    created_data = schemas.User.model_validate(created)
    return schemas.ResponseModel(status=True, data=created_data)

@app.get("/users/", response_model=schemas.ResponseModel)
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    users_data = [schemas.User.model_validate(u) for u in users]
    return schemas.ResponseModel(status=True, data=users_data)

@app.get("/users/{user_id}", response_model=schemas.ResponseModel)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        return schemas.ResponseModel(status=False, message="User not found")
    user_data = schemas.User.model_validate(user)
    return schemas.ResponseModel(status=True, data=user_data)

@app.put("/users/{user_id}", response_model=schemas.ResponseModel)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user)
    if not updated:
        return schemas.ResponseModel(status=False, message="User not found")
    updated_data = schemas.User.model_validate(updated)
    return schemas.ResponseModel(status=True, data=updated_data)

@app.delete("/users/{user_id}", response_model=schemas.ResponseModel)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        return schemas.ResponseModel(status=False, message="User not found")
    return schemas.ResponseModel(status=True, data={"deleted": True})


# Products

@app.post("/products/", response_model=schemas.ResponseModel)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    created = crud.create_product(db, product)
    created_data = schemas.Product.model_validate(created)
    return schemas.ResponseModel(status=True, data=created_data)

@app.get("/products/", response_model=schemas.ResponseModel)
def read_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    products_data = [schemas.Product.model_validate(p) for p in products]
    return schemas.ResponseModel(status=True, data=products_data)

@app.get("/products/{product_id}", response_model=schemas.ResponseModel)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        return schemas.ResponseModel(status=False, message="Product not found")
    product_data = schemas.Product.model_validate(product)
    return schemas.ResponseModel(status=True, data=product_data)

@app.put("/products/{product_id}", response_model=schemas.ResponseModel)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    if not updated:
        return schemas.ResponseModel(status=False, message="Product not found")
    updated_data = schemas.Product.model_validate(updated)
    return schemas.ResponseModel(status=True, data=updated_data)

@app.delete("/products/{product_id}", response_model=schemas.ResponseModel)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        return schemas.ResponseModel(status=False, message="Product not found")
    return schemas.ResponseModel(status=True, data={"deleted": True})

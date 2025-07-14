from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal

import logging

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- USERS --------------------

@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    created = crud.create_user(db, user)
    created_data = schemas.User.model_validate(created).model_dump()
    return JSONResponse(content={"status": True, "data": created_data})

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    users_data = [schemas.User.model_validate(u).model_dump() for u in users]
    return JSONResponse(content={"status": True, "data": users_data})

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        return JSONResponse(status_code=404, content={"status": False, "message": "User not found"})
    user_data = schemas.User.model_validate(user).model_dump()
    return JSONResponse(content={"status": True, "data": user_data})

@app.put("/users/{user_id}")
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user)
    if not updated:
        return JSONResponse(status_code=404, content={"status": False, "message": "User not found"})
    updated_data = schemas.User.model_validate(updated).model_dump()
    return JSONResponse(content={"status": True, "data": updated_data})

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        return JSONResponse(status_code=404, content={"status": False, "message": "User not found"})
    return JSONResponse(content={"status": True, "data": {"deleted": True}})


# -------------------- PRODUCTS --------------------

@app.post("/products/")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    logger.info(f"📥 Gelen veri (Postman'den): {product.model_dump()}")

    created = crud.create_product(db, product)

    logger.info(f"✅ Veritabanına kaydedilen ürün: {created.__dict__}")

    created_data = schemas.Product.model_validate(created).model_dump()
    return JSONResponse(content={"status": True, "data": created_data})

@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    products_data = [schemas.Product.model_validate(p).model_dump() for p in products]
    return JSONResponse(content={"status": True, "data": products_data})

@app.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        return JSONResponse(status_code=404, content={"status": False, "message": "Product not found"})
    product_data = schemas.Product.model_validate(product).model_dump()
    return JSONResponse(content={"status": True, "data": product_data})

@app.put("/products/{product_id}")
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    if not updated:
        return JSONResponse(status_code=404, content={"status": False, "message": "Product not found"})
    updated_data = schemas.Product.model_validate(updated).model_dump()
    return JSONResponse(content={"status": True, "data": updated_data})

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        return JSONResponse(status_code=404, content={"status": False, "message": "Product not found"})
    return JSONResponse(content={"status": True, "data": {"deleted": True}})

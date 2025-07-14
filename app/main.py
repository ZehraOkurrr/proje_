from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal
import logging

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# DB tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# DB session getter
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- COMPANY --------------------

@app.post("/companies/", response_model=schemas.ResponseModel[schemas.Company])
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    try:
        created = crud.create_company(db=db, company=company)
        return schemas.ResponseModel.success(data=created)
    except Exception as e:
        return schemas.ResponseModel.error(str(e))

@app.get("/companies/", response_model=schemas.ResponseModel[list[schemas.Company]])
def read_companies(db: Session = Depends(get_db)):
    companies = crud.get_companies(db)
    return schemas.ResponseModel.success(data=companies)

@app.get("/companies/{company_id}", response_model=schemas.ResponseModel[schemas.Company])
def read_company(company_id: int, db: Session = Depends(get_db)):
    company = crud.get_company(db, company_id)
    if not company:
        return schemas.ResponseModel.error("Company not found")
    return schemas.ResponseModel.success(data=company)

@app.put("/companies/{company_id}", response_model=schemas.ResponseModel[schemas.Company])
def update_company(company_id: int, company: schemas.CompanyBase, db: Session = Depends(get_db)):
    updated = crud.update_company(db, company_id, company)
    if not updated:
        return schemas.ResponseModel.error("Company not found")
    return schemas.ResponseModel.success(data=updated)

@app.delete("/companies/{company_id}", response_model=schemas.ResponseModel[dict])
def delete_company(company_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_company(db, company_id)
    if not deleted:
        return schemas.ResponseModel.error("Company not found")
    return schemas.ResponseModel.success(data={"deleted": True})

# -------------------- USERS --------------------

@app.post("/users/", response_model=schemas.ResponseModel[schemas.User])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    created = crud.create_user(db, user)
    return schemas.ResponseModel.success(data=created)

@app.get("/users/", response_model=schemas.ResponseModel[list[schemas.User]])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return schemas.ResponseModel.success(data=users)

@app.get("/users/{user_id}", response_model=schemas.ResponseModel[schemas.User])
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        return schemas.ResponseModel.error("User not found")
    return schemas.ResponseModel.success(data=user)

@app.put("/users/{user_id}", response_model=schemas.ResponseModel[schemas.User])
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user)
    if not updated:
        return schemas.ResponseModel.error("User not found")
    return schemas.ResponseModel.success(data=updated)

@app.delete("/users/{user_id}", response_model=schemas.ResponseModel[dict])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        return schemas.ResponseModel.error("User not found")
    return schemas.ResponseModel.success(data={"deleted": True})

# -------------------- PRODUCTS --------------------

@app.post("/products/", response_model=schemas.ResponseModel[schemas.Product])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    logger.info(f"📥 Gelen veri: {product.model_dump()}")
    created = crud.create_product(db, product)
    logger.info(f"✅ DB'ye eklenen: {created.__dict__}")
    return schemas.ResponseModel.success(data=created)

@app.get("/products/", response_model=schemas.ResponseModel[list[schemas.Product]])
def read_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return schemas.ResponseModel.success(data=products)

@app.get("/products/{product_id}", response_model=schemas.ResponseModel[schemas.Product])
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        return schemas.ResponseModel.error("Product not found")
    return schemas.ResponseModel.success(data=product)

@app.put("/products/{product_id}", response_model=schemas.ResponseModel[schemas.Product])
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    if not updated:
        return schemas.ResponseModel.error("Product not found")
    return schemas.ResponseModel.success(data=updated)

@app.delete("/products/{product_id}", response_model=schemas.ResponseModel[dict])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        return schemas.ResponseModel.error("Product not found")
    return schemas.ResponseModel.success(data={"deleted": True})

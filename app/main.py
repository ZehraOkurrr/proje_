from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal
from .utils import success_response, error_response, CustomJSONResponse
import logging

app = FastAPI(default_response_class=CustomJSONResponse)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- COMPANIES --------------------

@app.post("/companies/")
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    try:
        created = crud.create_company(db=db, company=company)
        return success_response(created, schema=schemas.Company)
    except Exception as e:
        return error_response(str(e))

@app.get("/companies/")
def read_companies(db: Session = Depends(get_db)):
    companies = crud.get_companies(db)
    return success_response(companies, schema=schemas.Company)

@app.get("/companies/{company_id}")
def read_company(company_id: int, db: Session = Depends(get_db)):
    company = crud.get_company(db, company_id)
    if not company:
        return error_response("Company not found")
    return success_response(company, schema=schemas.Company)

@app.put("/companies/{company_id}")
def update_company(company_id: int, company: schemas.CompanyBase, db: Session = Depends(get_db)):
    updated = crud.update_company(db, company_id, company)
    if not updated:
        return error_response("Company not found")
    return success_response(updated, schema=schemas.Company)

@app.delete("/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_company(db, company_id)
    if not deleted:
        return error_response("Company not found")
    return success_response({"deleted": True}, schema=schemas.GenericSuccess)

# -------------------- USERS --------------------

@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    created = crud.create_user(db, user)
    return success_response(created, schema=schemas.User)

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return success_response(users, schema=schemas.User)

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        return error_response("User not found")
    return success_response(user, schema=schemas.User)

@app.put("/users/{user_id}")
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user)
    if not updated:
        return error_response("User not found")
    return success_response(updated, schema=schemas.User)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        return error_response("User not found")
    return success_response({"deleted": True}, schema=schemas.GenericSuccess)

# -------------------- PRODUCTS --------------------

@app.post("/products/")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    logger.info(f"📥 Gelen veri: {product.model_dump()}")
    created = crud.create_product(db, product)
    logger.info(f"✅ DB'ye eklenen: {created.__dict__}")
    return success_response(created, schema=schemas.Product)

@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return success_response(products, schema=schemas.Product)

@app.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        return error_response("Product not found")
    return success_response(product, schema=schemas.Product)

@app.put("/products/{product_id}")
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    if not updated:
        return error_response("Product not found")
    return success_response(updated, schema=schemas.Product)

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        return error_response("Product not found")
    return success_response({"deleted": True}, schema=schemas.GenericSuccess)

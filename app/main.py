from fastapi import FastAPI, Depends, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import models, schemas, crud
from .database import engine, SessionLocal
from .utils import success_response, error_response, CustomJSONResponse
import logging
from fastapi.exception_handlers import request_validation_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError


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

def handle_exception(e):
    if isinstance(e, ValidationError):
        first_error = e.errors()[0]
        return error_response(first_error.get("msg", "Invalid input"), status_code=422)

    message = getattr(e, "detail", str(e))
    return error_response(message)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    simple_message = first_error.get("msg", "Invalid input")
    return error_response(simple_message, status_code=422)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return error_response(exc.detail, status_code=exc.status_code)






# -------------------- COMPANIES --------------------

@app.post("/companies/")
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    try:
        created = crud.create_company(db=db, company=company)
        return success_response(created, schemas.Company)
    except Exception as e:
        return handle_exception(e)

@app.get("/companies/")
def read_companies(db: Session = Depends(get_db)):
    companies = crud.get_companies(db)
    return success_response(companies, schemas.Company)

@app.get("/companies/{company_id}")
def read_company(company_id: int, db: Session = Depends(get_db)):
    company = crud.get_company(db, company_id)
    if not company:
        return error_response("Company not found")
    return success_response(company, schemas.Company)

@app.put("/companies/{company_id}")
def update_company(company_id: int, company: schemas.CompanyBase, db: Session = Depends(get_db)):
    updated = crud.update_company(db, company_id, company)
    if not updated:
        return error_response("Company not found")
    return success_response(updated, schemas.Company)

@app.delete("/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_company(db, company_id)
    if not deleted:
        return error_response("Company not found")
    return success_response({"deleted": True}, schema=None)





# -------------------- USERS --------------------

@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        created = crud.create_user(db, user)
        return success_response(created, schemas.User)
    except Exception as e:
        return handle_exception(e)

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return success_response(users, schemas.User)

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        return error_response("User not found")
    return success_response(user, schemas.User)

@app.put("/users/{user_id}")
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user)
    if not updated:
        return error_response("User not found")
    return success_response(updated, schemas.User)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        return error_response("User not found")
    return success_response({"deleted": True}, schema=None)





# -------------------- PRODUCTS --------------------

@app.post("/products/")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"📥 Gelen veri: {product.model_dump()}")
        created = crud.create_product(db, product)
        logger.info(f"✅ DB'ye eklenen: {created.__dict__}")
        return success_response(created, schemas.Product)
    except Exception as e:
        return handle_exception(e)

@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return success_response(products, schemas.Product)

@app.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        return error_response("Product not found")
    return success_response(product, schemas.Product)

@app.put("/products/{product_id}")
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    if not updated:
        return error_response("Product not found")
    return success_response(updated, schemas.Product)

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        return error_response("Product not found")
    return success_response({"deleted": True}, schema=None)





# -------------------- CATEGORIES --------------------

@app.post("/categories/")
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    try:
        created = crud.create_category(db, category)
        return success_response(created, schemas.Category)
    except Exception as e:
        return handle_exception(e)

@app.get("/categories/")
def read_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return success_response(categories, schemas.Category)

@app.get("/categories/{category_id}")
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if not category:
        return error_response("Category not found")
    return success_response(category, schemas.Category)

@app.put("/categories/{category_id}")
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    updated = crud.update_category(db, category_id, category)
    if not updated:
        return error_response("Category not found")
    return success_response(updated, schemas.Category)

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_category(db, category_id)
    if not deleted:
        return error_response("Category not found")
    return success_response({"deleted": True}, schema=None)

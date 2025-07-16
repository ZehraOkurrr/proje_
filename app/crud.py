from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from . import models, schemas

# Yardımcı hata yöneticisi
def handle_db_exceptions(e):
    message = str(e.orig).lower()
    if "foreign key constraint" in message:
        raise HTTPException(status_code=400, detail="Foreign key constraint failed.")
    elif "duplicate" in message or "unique" in message:
        raise HTTPException(status_code=400, detail="Duplicate entry.")
    elif "null" in message:
        raise HTTPException(status_code=400, detail="Missing required field.")
    else:
        raise HTTPException(status_code=400, detail="Database integrity error.")

# USERS
def get_users(db: Session):
    return db.query(models.User).options(joinedload(models.User.company)).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).options(joinedload(models.User.company)).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, age=user.age)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        handle_db_exceptions(e)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected database error occurred.")

def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.age = user.age
        try:
            db.commit()
            db.refresh(db_user)
        except IntegrityError as e:
            db.rollback()
            handle_db_exceptions(e)
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Unexpected database error occurred.")
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        try:
            db.delete(db_user)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Unexpected database error occurred.")
    return db_user

# COMPANY
def create_company(db: Session, company: schemas.CompanyCreate):
    existing = db.query(models.Company).filter_by(user_id=company.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="This user already has a company.")

    existing_name = db.query(models.Company).filter_by(name=company.name).first()
    if existing_name:
        raise HTTPException(status_code=400, detail="This company name is already used.")

    db_company = models.Company(**company.dict())
    try:
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e.orig).lower():
            raise HTTPException(status_code=400, detail="User not found.")
        handle_db_exceptions(e)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected database error occurred.")

def get_companies(db: Session):
    return db.query(models.Company).options(joinedload(models.Company.user)).all()

def get_company(db: Session, company_id: int):
    return db.query(models.Company).options(joinedload(models.Company.user)).filter(models.Company.id == company_id).first()

def update_company(db: Session, company_id: int, company: schemas.CompanyBase):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not db_company:
        return None
    db_company.name = company.name
    try:
        db.commit()
        db.refresh(db_company)
        return db_company
    except IntegrityError as e:
        db.rollback()
        handle_db_exceptions(e)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected database error occurred.")

def delete_company(db: Session, company_id: int):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not db_company:
        return None
    try:
        db.delete(db_company)
        db.commit()
        return db_company
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected database error occurred.")

# PRODUCTS
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        color=product.color,
        quantity=product.quantity,
        user_id=product.user_id
    )
    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        if product.category_ids:
            categories = db.query(models.Category).filter(models.Category.id.in_(product.category_ids)).all()
            db_product.categories = categories
            db.commit()

        return db_product
    except IntegrityError as e:
        db.rollback()
        handle_db_exceptions(e)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected database error occurred.")

def get_products(db: Session):
    return db.query(models.Product).options(joinedload(models.Product.categories)).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).options(joinedload(models.Product.categories)).filter(models.Product.id == product_id).first()

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.color = product.color
    db_product.quantity = product.quantity
    db_product.user_id = product.user_id
    try:
        if product.category_ids:
            categories = db.query(models.Category).filter(models.Category.id.in_(product.category_ids)).all()
            db_product.categories = categories
        else:
            db_product.categories = []

        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError as e:
        db.rollback()
        handle_db_exceptions(e)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected database error occurred.")

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        return None
    try:
        db.delete(db_product)
        db.commit()
        return db_product
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected database error occurred.")


# -------------------- CATEGORY --------------------

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError as e:
        db.rollback()
        handle_db_exceptions(e)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected database error occurred.")

def get_categories(db: Session):
    return db.query(models.Category).all()

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def update_category(db: Session, category_id: int, category: schemas.CategoryCreate):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        return None
    db_category.name = category.name
    try:
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError as e:
        db.rollback()
        handle_db_exceptions(e)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected database error occurred.")

def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        return None
    try:
        db.delete(db_category)
        db.commit()
        return db_category
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected database error occurred.")

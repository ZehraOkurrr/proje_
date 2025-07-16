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

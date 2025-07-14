from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from . import models, schemas

# USERS

def get_users(db: Session):
    return db.query(models.User).options(joinedload(models.User.company)).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).options(joinedload(models.User.company)).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.age = user.age
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
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
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_companies(db: Session):
    return db.query(models.Company).options(joinedload(models.Company.user)).all()

def get_company(db: Session, company_id: int):
    return db.query(models.Company).options(joinedload(models.Company.user)).filter(models.Company.id == company_id).first()


def update_company(db: Session, company_id: int, company: schemas.CompanyBase):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not db_company:
        return None
    db_company.name = company.name
    db.commit()
    db.refresh(db_company)
    return db_company


def delete_company(db: Session, company_id: int):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not db_company:
        return None
    db.delete(db_company)
    db.commit()
    return db_company

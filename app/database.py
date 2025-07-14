from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "mysql_db1"  # Docker içindeki servis adı
DB_PORT = "3306"      # Docker içindeki MySQL portu
DB_NAME = "proje_db"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

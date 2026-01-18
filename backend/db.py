from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Database URL (SQLite file)
# 2. Create database engine
# 3. Create a SessionLocal class
# 4. Base class for database models
# 5. Dependency to get DB session

DATABASE_URL = "sqlite:///./receipts.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

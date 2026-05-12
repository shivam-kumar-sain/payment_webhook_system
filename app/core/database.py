from sqlalchemy import create_engine,DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase,Mapped, mapped_column
from core.config import settings
from datetime import datetime


"""
    --------------------------------------------------
    Database URL (ENV se)
    --------------------------------------------------
"""
DATABASE_URL = settings.database_url

"""
    --------------------------------------------------
    Engine (DB connection pool)
    --------------------------------------------------
"""
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, 
    pool_size=10,
    max_overflow=20,
    echo=False,        
)

"""
    --------------------------------------------------
    Session factory
    --------------------------------------------------
"""
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

"""
    --------------------------------------------------
    Base class (for db models)
    --------------------------------------------------
"""
class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)

"""
    --------------------------------------------------
    Dependency (for api's)
    --------------------------------------------------
"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

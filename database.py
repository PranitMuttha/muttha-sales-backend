import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Look for the Render Environment Variable
# If it's not found, it falls back to your local setup
raw_url = os.getenv("DATABASE_URL")

if raw_url:
    # Render uses "postgres://", but SQLAlchemy requires "postgresql://"
    SQLALCHEMY_DATABASE_URL = raw_url.replace("postgres://", "postgresql://", 1)
else:
    # Your local fallback
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/muttha_sales"

# 2. Create the engine
# Note: "check_same_thread" is only needed for SQLite, but safe to leave out for Postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

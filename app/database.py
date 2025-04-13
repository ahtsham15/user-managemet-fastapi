from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5433/user_auth_fastapi"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=True, bind=engine)

Base = declarative_base()
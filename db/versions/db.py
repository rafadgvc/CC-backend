from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os



Base = declarative_base()

def create_session():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set. Ensure it is configured in your environment.")
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()

session = create_session()


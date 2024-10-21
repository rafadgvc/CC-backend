from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os




url_object = URL.create(
    "postgresql",
    username="root",
    password="1a2b3c4d5e!$",  # plain (unescaped) text
    host="localhost",
    database="postgres",
    port="5432"
)


Base = declarative_base()

def create_db():
    if os.getenv("FLASK_ENV") == "testing":
        database_url = "sqlite:///:memory:"
    else:
        database_url = os.getenv("DATABASE_URL", "postgresql://root:1a2b3c4d5e!$@localhost:5432/postgres")

    engine = create_engine(url_object)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


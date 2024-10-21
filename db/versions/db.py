from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os



Base = declarative_base()

def create_session():
    # Escoge la base de datos según el entorno
    if os.getenv('FLASK_ENV') == 'testing':
        engine = create_engine('sqlite:///:memory:')
    else:
        engine = create_engine('postgresql://root:1a2b3c4d5e!$@localhost:5432/postgres')

    Session = sessionmaker(bind=engine)
    return Session()

# Inicializa la sesión de la base de datos
session = create_session()

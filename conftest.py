import pytest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from models.user.user import User
from db.versions.db import Base
from app import app as flask_app
from db.versions.db import create_db
import os

# Fixture para la aplicación Flask
@pytest.fixture
def app():
    os.environ["FLASK_ENV"] = "testing"
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "dont-look-at-me-this-is-a-secret!",
    })

    with flask_app.app_context():
        yield flask_app

# Fixture para el cliente de pruebas
@pytest.fixture
def client(app):
    return app.test_client()

# Fixture para la base de datos y la sesión
@pytest.fixture
def db(app):
    Session = create_db("sqlite:///:memory:")

    Base.metadata.create_all(Session.bind)

    session = Session()

    yield session

    session.rollback()
    session.close()


    Base.metadata.drop_all(Session.bind)


# Fixture para crear un usuario de prueba
@pytest.fixture
def test_user(db):
    user_data = {
        "email": "sinapsido@gmail.com",
        "name": "Sinápsido Dicinodonte",
        "password": "P374l D4nC3"
    }
    user_schema = User.insert_user(
        session=db,
        email=user_data['email'],
        name=user_data['name'],
        password=user_data['password']
    )
    return user_schema
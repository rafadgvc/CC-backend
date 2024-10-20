import bcrypt
import pytest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from models.user.user import User
from app import app as flask_app
from db.versions.db import Base, create_session
import os

# Fixture para la aplicación Flask
@pytest.fixture
def app():
    os.environ["FLASK_ENV"] = "testing"
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "EXAMPLE_KEY",
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
    session = create_session()

    Base.metadata.create_all(session.bind)

    yield session

    session.rollback()
    session.close()
    Base.metadata.drop_all(session.bind)

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
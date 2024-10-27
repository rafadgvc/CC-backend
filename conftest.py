import bcrypt
import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from models.node.node import Node
from models.subject.subject import Subject
from models.user.user import User
from app import app as flask_app
from db.versions.db import Base, create_session
import os

from secret import PASSWORD_SALT


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


# Fixture para crear un usuario de ejemplo
@pytest.fixture
def example_user(db):
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


# Fixture para crear una asignatura de ejemplo
@pytest.fixture
def example_subject(db, example_user):
    subject_data = {
        "name": "Geografía",
        "user_id": example_user.get('id'),
    }
    subject = Subject.insert_subject(
        session=db,
        name=subject_data.get('name')
    )
    return subject


# Fixture para crear un nodo de ejemplo asociado a una asignatura
@pytest.fixture
def example_node(db, example_subject):
    node_data = {
        "name": "Teselia",
        "subject_id": example_subject.get("id"),
        "parent_id": example_subject.get("id")
    }
    node = Node.insert_node(
        session=db,
        name=node_data.get('name'),
        subject_id=node_data.get('subject_id'),
        parent_id=node_data.get('parent_id')
    )
    return node

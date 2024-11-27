import bcrypt
import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from models.exam.exam import Exam
from models.node.node import Node
from models.question import Question
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
        "parent_id": -1
    }
    node = Node.insert_node(
        session=db,
        name=node_data.get('name'),
        subject_id=node_data.get('subject_id'),
        parent_id=node_data.get('parent_id')
    )
    return node


# Fixture para crear una pregunta de ejemplo
@pytest.fixture
def example_question(db, example_subject, example_node):
    node_ids = []
    node_ids.append(example_node.get("id"))
    question_data = {
        "title": "Explique brevemente la leyenda de los dos reyes de Teselia",
        "subject_id": example_subject.get("id"),
        "difficulty": 4,
        "time": 10,
        "parametrized": False,
        "node_ids": node_ids,
        "type": "desarrollo",
        "answers": [],
        "question_parameters": [],
        "active": True
    }
    question = Question.insert_question(
        session=db,
        title=question_data.get('title'),
        subject_id=question_data.get('subject_id'),
        difficulty=question_data.get('difficulty'),
        node_ids=question_data.get('node_ids'),
        type=question_data.get('type'),
        answers=question_data.get('answers'),
        question_parameters={"items": []},
        time=question_data.get('time'),
        active=question_data.get('active'),
        parametrized=question_data.get('parametrized')
    )
    return question

# Fixture para crear un examen de ejemplo
@pytest.fixture
def example_exam(db, example_subject, example_node, example_question):
    node_ids = []
    node_ids.append(example_node.get("id"))
    question_data = {
        "id": example_question.get("id"),
        "title": "Explique brevemente la leyenda de los dos reyes de Teselia",
        "subject_id": example_subject.get("id"),
        "difficulty": 4,
        "time": 10,
        "parametrized": False,
        "node_ids": node_ids,
        "type": "desarrollo",
        "answers": [],
        "question_parameters": [],
        "active": True,
        "section_number": 1
    }
    questions=[]
    questions.append(question_data)
    exam_data = {
        "title" : "Examen de repaso de Historia",
        "questions": questions,
        "subject_id": example_subject.get("id")
    }
    exam = Exam.insert_exam(
        session=db,
        title=exam_data.get('title'),
        questions=exam_data.get('questions'),
        subject_id=exam_data.get('subject_id')
    )
    return exam

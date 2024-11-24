import pytest
from sqlalchemy import text
from sqlalchemy.engine.reflection import Inspector

from app import app
from db.versions.db import create_session, Base
from models.user.user import User


@pytest.fixture
def client():
    """Crea un cliente de pruebas para la aplicación Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def setup_test_data():
    """Prepara datos de prueba en la base de datos."""
    session = create_session()
    user = User.insert_user(session, email="test@example.com", name="Test User", password="12345")
    return user


@pytest.fixture(autouse=True)
def clean_database():
    """Limpia la base de datos en un orden específico."""
    session = create_session()

    # Orden específico de tablas
    ordered_tables = [
        "result", "exam_question_association", "exam", "answer", "question_parameter", "node_question_association",
        "question", "node", "subject", "user"
    ]

    try:
        inspector = Inspector.from_engine(session.get_bind())

        # Desactivar todas las restricciones de las tablas involucradas
        for table_name in ordered_tables:
            if table_name in Base.metadata.tables:
                foreign_keys = inspector.get_foreign_keys(table_name)
                for fk in foreign_keys:
                    fk_name = fk['name']
                    if fk_name:
                        session.execute(text(f'ALTER TABLE {table_name} DROP CONSTRAINT {fk_name};'))
        session.commit()

        # Eliminar los datos en el orden definido
        for table_name in ordered_tables:
            if table_name in Base.metadata.tables:
                table = Base.metadata.tables[table_name]
                session.execute(table.delete())  # Borra todos los registros de la tabla
        session.commit()

    except Exception as e:
        # Si ocurre un error, deshacer los cambios
        session.rollback()
        raise e

    finally:
        # Reactivar las restricciones dinámicamente
        for table_name in ordered_tables:
            if table_name in Base.metadata.tables:
                foreign_keys = inspector.get_foreign_keys(table_name)
                for fk in foreign_keys:
                    fk_name = fk['name']
                    if fk_name:
                        ref_table = fk['referred_table']
                        local_cols = ', '.join(fk['constrained_columns'])
                        ref_cols = ', '.join(fk['referred_columns'])
                        session.execute(text(
                            f'ALTER TABLE {table_name} ADD CONSTRAINT {fk_name} FOREIGN KEY ({local_cols}) REFERENCES {ref_table} ({ref_cols});'
                        ))
        session.commit()


@pytest.fixture
def setup_user():
    """Crea un usuario de prueba en la base de datos."""
    session = create_session()
    user = User.insert_user(
        session=session,
        email="ceratopsia@example.com",
        name="Ceratopsia Cerapoda",
        password="1R0n d3f3n53"
    )
    yield user

    session.query(User).filter_by(email="ceratopsia@example.com").delete()
    session.commit()


@pytest.fixture
def auth_token(client, setup_user):
    """Obtiene un token JWT para usar en los tests."""
    login_payload = {
        "email": "ceratopsia@example.com",
        "password": "1R0n d3f3n53"
    }
    response = client.post('/user/login', json=login_payload)
    assert response.status_code == 200
    return response.json["access_token_cookie"]


@pytest.fixture
def setup_subject(client, auth_token):
    """Crea una Asignatura de prueba."""
    payload = {"name": "Geografía"}
    response = client.post(
        '/subject',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=payload
    )
    assert response.status_code == 200
    return response.json


@pytest.fixture
def setup_node(client, auth_token, setup_subject):
    """Crea un Nodo de prueba."""
    payload = {
        "name": "Teselia",
        "subject_id": setup_subject.get('id'),
        "parent_id": -1,
    }
    response = client.post(
        '/node',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=payload
    )
    assert response.status_code == 200
    return response.json


@pytest.fixture
def setup_question(client, auth_token, setup_subject, setup_node):
    """Crea una pregunta de prueba."""

    payload = {
        "title": "Explique brevemente la leyenda de los reyes de Teselia.",
        "subject_id": setup_subject.get("id"),
        "node_ids": [setup_node.get("id")],
        "active": True,
        "time": 10,
        "difficulty": 4,
        "type": "desarrollo",
        "question_parameters": {
            "items": [],
            "total": 0
        },
        "answers": {
            "items": [],
            "total": 0
        }
    }
    response = client.post(
        '/question',
        headers={"Authorization": f"Bearer {auth_token}"},
        json=payload
    )
    assert response.status_code == 200
    return response.json
